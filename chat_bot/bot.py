import os
from datetime import datetime as dt

import warnings
import transformers
from transformers import logging
import torch

class Calm_Bot():

    def __init__(self, weight_path="./weights/model_state_V4_6.pt", print_info=True):
        logging.set_verbosity_error()
        warnings.filterwarnings('ignore')

        self.print_info = print_info
        self.weight_path = weight_path
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

    def set_device(self):
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')

    def load_tokenizer(self):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2", padding_side="right")
        self.tokenizer.add_special_tokens({  "pad_token": "<pad>",
                                             "eos_token": "<end>",
                                             "sep_token": "<sep>"})
        self.tokenizer.add_tokens(["<bot>"])

    def load_model(self):
        self.model = transformers.GPT2LMHeadModel.from_pretrained("gpt2")  #, config=self.config
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.eval()
        self.model = self.model.to(self.device)
        if self.print_info:
            print(f"loading weights from '{self.weight_path}'")
        self.model.load_state_dict(torch.load(self.weight_path, map_location=self.device))

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
                                            max_length=self.max_length)
        
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
    

        self.prompt += f"<sep>{output}"
        self.history += f"\n\nuser: {user_input}\n\nbot: {output}"
        return output

    def set_topic(self, topic):
        self.topic = topic

    def save_history(self, name=None):
        if self.history != "":
            if type(name) != str:
                name = f"RIS_experience_{dt.now().strftime('%Y-%m-%d %H')}_{self.topic}"
            counter = 2
            while name in os.listdir("./histories"):
                name = f"RIS_experience_{dt.now().strftime('%Y-%m-%d %H')}_{self.topic}_{counter}"
            
            with open(f"./histories/{name}", "w") as f:
                f.write(self.history)

    def get_history(self, name=None):
        return self.history

    def reload(self):
        self.history = ""
        self.prompt = ""
        self.set_device()
        self.load_tokenizer()
        self.load_model()





