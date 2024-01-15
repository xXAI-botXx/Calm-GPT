import os
from datetime import datetime as dt

import warnings
import transformers
from transformers import logging
import torch

class Calm_Bot():

    def __init__(self, dir_path=".", print_info=True, offline=True, model_version="V6_8"):
        logging.set_verbosity_error()
        warnings.filterwarnings('ignore')

        self.print_info = print_info
        self.model_version = model_version
        self.offline = offline
        self.dir_path = dir_path
        self.create_dir_paths()
        self.max_length = 1024
        self.history = ""
        self.prompt = ""
        self.past = None
        if self.print_info:
            print("setting device...")
        self.set_device()
        if self.print_info:
            print("loading tokenizer...")
        self.load_tokenizer()
        if self.print_info:
            print("loading GPT-2 model...")
        self.load_model()

    def create_dir_paths(self):
        try:
            os.makedirs(f"{self.dir_path}/histories")
        except Exception:
            pass

    def set_device(self):
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

    def load_tokenizer(self):
        if self.offline:
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(f"{self.dir_path}/tokenizer", padding_side="right")
        else:
            self.tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2", padding_side="right")
        self.tokenizer.add_special_tokens({  "pad_token": "<pad>",
                                             "eos_token": "<end>",
                                             "sep_token": "<sep>"})
        self.tokenizer.add_tokens(["<bot>"])

    def load_model(self):
        if self.offline:
            self.model = transformers.GPT2LMHeadModel.from_pretrained(f"{self.dir_path}/model")
        else:
            self.model = transformers.GPT2LMHeadModel.from_pretrained("gpt2")
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.eval()
        self.model = self.model.to(self.device)
        if self.print_info:
            print(f"loading weights from '{self.dir_path}/weights/model_state_{self.model_version}.pt'")
        self.model.load_state_dict(torch.load(f"{self.dir_path}/weights/model_state_{self.model_version}.pt", map_location=self.device))

    def inference(self, prompt:str, clear_output=True, print_input=False, print_output=False):
        user_input = prompt
        if len(self.prompt) == 0:
            self.prompt += f"{prompt}"
        else:
            self.prompt += f"<sep>{prompt}"
        if print_input:
            print(f"{self.prompt}<bot>")
        prompt = self.tokenizer(f"{self.prompt}<bot>",  truncation=True, 
                                                        return_tensors="pt", 
                                                        #max_length=self.max_length, 
                                                        padding=True)
        X = prompt["input_ids"].to(self.device)
        a = prompt["attention_mask"].to(self.device)
        with torch.no_grad():
            output = self.model.generate(X, attention_mask=a, 
                                            pad_token_id=self.tokenizer.pad_token_id,
                                            do_sample=True, 
                                            max_length=self.max_length)  #*2
        
        if print_output:
            _ = self.tokenizer.decode(output[0], skip_special_tokens=False)
            if type(_) == list and len(_) == 1:
                _ = _[0]
            print(_)

        output = self.tokenizer.decode(output[0], skip_special_tokens=False)

        if type(output) == list and len(output) == 1:
            output = output[0]

        if clear_output:
            start_idx = None
            end_idx = None
            for idx in range(0, len(output)-5):
                cur_word = output[idx:idx+5]
                if cur_word == "<bot>":
                    start_idx = idx+5
                elif cur_word in ["<end>", "<pad>"]:
                    end_idx = idx

                if type(start_idx) == int and type(end_idx) == int:
                    break                

            # check if cleaning worked, else try something else
            if type(start_idx) == int and type(end_idx) == int:
                output = output[start_idx:end_idx]
            else:
                if self.print_info:
                    print("There are problem during clearing the output.")

                if "<bot>" in output:
                    output = "".join(output.split("<bot>")[1:])

                if "<end>" in output:
                    output = output.split("<end>")[0]

                if "<pad>" in output:
                    output = output.split("<pad>")[0]

                if "<sep>" in output:
                    output = output.replace("<sep>", ". ")
    

        self.prompt += f"<sep>{output}"
        return output

    def set_topic(self, topic):
        self.topic = topic

    def save_history(self, path="./histories", name=None, override=False):
        if type(name) != str:
            name = f"chat {dt.now().strftime('%Y-%m-%d %H_%M')}.txt"
        if not name.endswith(".txt"):
            name += ".txt"
        counter = 2
        if override == False:
            while name in os.listdir(path):
                name = f"{name} {counter}.txt"
        
        with open(f"{path}/{name}", "w") as f:
            f.write(self.history)
        return name

    def load_histories(self, path="./histories"):
        histories = []
        for i in os.listdir(path):
            if len(i) > 0:
                if i.endswith(".txt"):
                    histories += [".".join(i.split(".")[:-1])]
                else:
                    histories += [i]
        return histories

    def load_history(self, path, name):
        self.reload()
        chat = self.get_history(path, name)
        self.prompt = ""
        for i, text in enumerate(chat):
            if i == 0:
                self.prompt += f"{text}"
            else:
                self.prompt += f"<sep>{text}"

    def get_history(self, path, name):
        if not name.endswith("txt"):
            name += ".txt"
        try:
            with open(f"{path}/{name}", "r") as f:
                history = f.read()
        except Exception:
            name = ".".join(name.split(".")[:-1])
            with open(f"{path}/{name}", "r") as f:
                history = f.read()

        history = history.split("\n\n")
        return_history = []
        for chat_idx in range(0, len(history)):
            if len(history[chat_idx]) > 0:
                if ":" in history[chat_idx]:
                    return_history += [":".join(history[chat_idx].split(":")[1:])]
                else:
                    return_history += [history[chat_idx]]
        return return_history

    def del_history(self, path, name):
        if not name.endswith("txt"):
            name += ".txt"

        try:
            os.remove(f"{path}/{name}")
        except FileNotFoundError:
            print(f"The file {file_path} are not found.")
        except Exception as e:
            print(f"Error during deleting the file: {e}")

    def add_to_history(self, is_user, message):
        if is_user:
            self.history += f"\n\nuser: {message}"
        else:
            self.history += f"\n\nbot: {message}"

    def save_model(self, empty_top_dir_path):
        # model
        model_path = f"{empty_top_dir_path}/model"
        os.makedirs(model_path)
        bot.model.save_pretrained(model_path)
        # tokenizer
        tokenizer_path = f"{empty_top_dir_path}/tokenizer"
        os.makedirs(tokenizer_path)
        bot.tokenizer.save_pretrained(tokenizer_path)
        # weights
        weights_path = f"{empty_top_dir_path}/weights"
        os.makedirs(weights_path)
        torch.save(model, f"{weights_path}/model_state_{self.model_version}.pt")
        return model_path, tokenizer_path, weights_path 

    def reload(self):
        self.history = ""
        self.prompt = ""
        self.set_device()
        self.load_tokenizer()
        self.load_model()





