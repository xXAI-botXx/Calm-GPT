<img src="logo.jpeg"></img>

<h1 style="text-align:center">Your calm down bot</h1>

<h2 style="text-align:center">☀️ The bot you wish was your therapist🏖️</h2>



Content:

- [Tags](#tags)
- [Description](#description)
- [Definition Talk Down](#definition-talk-down)
- [Project Milestones](#project-milestones)
- [Advantages and Disadvantages](#advantages-and-disadvantages)
- [Fine-Tuning Data](#fine-tuning-data)
- [Feature](#feature)
- [Branches](#branches)
- [Fine-Tuning](#fine-tuning)
- [Second Fine-Tuning](#second-fine-tuning)
- [Hardware](#hardware)
- [Evaluation](#evaluation)
- [Result](#result)



### Tags

- chatbot
- english
- GPT2 finetuning
- anxiety/stress/....
- traindata ChatGPT3.5 generated



### Description

A GPT2 model is to be extended to a new task via transfer learning. The GPT2 model is to be fine-tuned so that it acts as a "talk down" for anxiety/panic attacks. <br>
The model should therefore act as a chatbot. The communication participant should be positively encouraged and reassured.
The functionality of the bot is therefore similar to Eliza.<br>
The language is English and the model is to be deployed as a chatbot on Discord.<br>
The training data requires positive conversations that are relaxed and reassuring. The conversation should be sensitive and emotional, but with a certain lightness.<br>
The chatbot should therefore make reassuring statements at the end. It should remain rational and focus on the "here and now". It could possibly teach small tasks/relaxation techniques.<br>
Since such training data is difficult to obtain, ChatGPT is used to generate the data.<br>

<br>

The GPT3 model would actually be used for this, but this is associated with costs, so the decision was made to use the GPT2 model.<br>




### Project Milestones
- Traindata Commands are implemented
- Traindata (dialogs) with ChatGPT are generated
- A GPT2 model was trained/finetuned with the training data
- The bot got deployed on Discord over replit



### Advantages and Disadvantages

Pros:
- for free
- every time
- everywhere where
- 100% private



Cons:
- Answers can be similiar and not creative enough
- May not answer well every time
- Can give wrong tips and advises



### Fine-Tuning Data

For the data I use ChatGPT to generate my data. Therefore I need to prepare different commands to get the data. Also I have to program which picks different commands and calls ChatGPT over API.



Example Commands:

```
Erstelle einen Dialog, in dem eine Person über ihre Ängste spricht und die andere Person versucht, sie mit einer beruhigenden Visualisierungstechnik zu trösten.
The Questions and answer also can be very short, like in reality. Write only the Dialog no other message. Write the chat on english with really short answers and use following format:
Person A: Hey 
Person B: Hey, how are you? 
Person A: ... 
... 
```

``````
Erstelle einen Dialog, in dem eine Person über ihre Ängste spricht und die andere Person versucht, sie mit einer beruhigenden Visualisierungstechnik zu trösten.
The Questions and answer also can be very short, like in reality. Write only the Dialog no other message. Write the chat on english with really short answers and use following format:
Person A: Hey 
Person B: Hey, how are you? 
Person A: ... 
...
``````



This project shows, that there are good reasons to use ChatGPT for DataGeneration. In a half day you can generate your dream NLP dataset, but you have to pay money and have to setup up everything also different commands (you can use my work if it is helpful). In a nutshell:



Pro:

- Fast Datageneration
- Specific NLP-Data
- No license problems
- Very cheap



Con:

- Maybe too generic



**Total traindata creation time:**    

- 0 Days    
- 7 Hours 
- 5 Minutes 
- 52 Seconds



=> Created 1630 Training-Dialogs.



Results in 11.147 Input-Output Pairs!



To access the Openai API (now 05.01.2024), you can use following code:

```python
from openai import OpenAI

with open("./API_KEY.txt", "r") as f:
  API_KEY = f.read()
client = OpenAI(api_key=API_KEY)

def request_gpt3(message):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    return response.choices[0].message.content
```

 You have to create an API-Code on the official website and have to pay some money for the usage. I saved my API-KEY in a text file and just loaded it, as shown in the code. Don't forget to add the API_KEY.txt to your gitignore file.



Now it's important to build a loop, in which different commands are selected. Different commands leads to different answeres, so it's very important to have many commands. Then it is also important to save the answer from the ChatGPT model into a file. How exactly is up to you. I did it like [this (data_generation.ipynb)](./data_generation.ipynb). 

As pseudocode it can look like:

``````pseudocode
while True:
	command = choose_command()
	answer = request_gpt3(command)
	save_answer_in_file(answer)
``````



### Features

- problem talking
- calm talking
- visualization stories
- chatting



### Branches

- main = contains the trained model and scripts to train the model
- every other branch is a platform integration (Discord, Mobile, Desktop,...)



### Fine-Tuning

For the fine-tuning there are many things to respect. Here the most important facts. I used the Google Collab environment with the NVIDIA Tesla V100. More hardware details are shown in the next chapter.

For the optimizer I orintated on models like GPT-3 and used the Adam-Optimizer. I choose a small learnrate 1*e-4 to generalise well. I expect that a low epoch-rate will be fine, because the data is partwise very similiar, so in one epoch the model saw the same data more than one times, I don't know how often exactly. 

The Batch-Size is 4, which is very small, but my available GPU-RAM had no more capacity.

To contain the context it was important to add the context of the conversation to the input prompt. It is questionable how good this works. Currently it's not sure how many messages are given by the given 1024 tokens. Also it's not clear, if the user and bot inputs markings are working like I wish (I added marks to itlike: ...\<sep>... -> see below for a indeepth example). And finally it could happen, that messages are splitted somewhere and the context could propably change through this process. Also the missing of start and/or end token can hinder the model, but I expect this is not a problem, since the provided informations of these tokens are not so important (from my perspective). 



Tokens as described in the [documentation](https://huggingface.co/transformers/v3.0.2/main_classes/tokenizer.html):

**bos_token** (*-*) – (Optional) string: a beginning of sentence token. Will be associated to `self.bos_token` and `self.bos_token_id`

**eos_token** (*-*) – (Optional) string: an end of sentence token. Will be associated to `self.eos_token` and `self.eos_token_id`

**sep_token** (*-*) – (Optional) string: a separation token (e.g. to separate context and query in an input sequence). Will be associated to `self.sep_token` and `self.sep_token_id`

**pad_token** (*-*) – (Optional) string: a padding token. Will be associated to `self.pad_token` and `self.pad_token_id`



Our Input with context will looks like:

> Hey, I've been feeling really down lately. I just can't seem to find any motivation or purpose in my life.**<sep>**I completely understand how you feel. I went through a similar phase a while back. I had lost all sense of direction and felt like my life lacked purpose. But then I came across this incredible story that really inspired me.**<sep>**What was the story about?**<sep>**It was about a man named Nick Vujicic. He was born without arms and legs, and faced numerous challenges and obstacles throughout his life. Despite all that, he never let his disabilities define him. Instead, he used his setbacks as fuel to achieve incredible things. He became a motivational speaker, inspiring millions of people around the world.**<sep>**That's really inspiring. But how did he manage to find motivation and purpose in his life?**<sep>**Well, Nick didn't let his circumstances determine his happiness or success. He believed that true happiness and purpose come from within, and he focused on developing a positive mindset. He found joy in helping others and making a difference in their lives. He embraced his unique situation and used it as a platform to inspire others.**<sep>**That's amazing. But I still struggle to find that inner motivation and purpose in my own life.**<bot>**I think the key is to start small and take little steps towards finding what truly makes you happy. Explore different interests, set goals for yourself, and surround yourself with positive and supportive people. Remember, everyone's journey is different, and it's okay to take your time to discover your passion and purpose. Believe in yourself and your abilities, and never give up.



> Hey, I've been feeling really overwhelmed lately and I think I might have Separation Anxiety Disorder.**<bot>**Oh, I'm sorry to hear that. What exactly are you experiencing?



I decided to only use the sep, pad and a special bot token. The sep-token will help the model to understand the context, the pad token for the padding (because the input need the same length). There is also a special bot token that allows the model to know which part is his part and can learn it.

The start token is not used, because it will be cutted away when the input is too big and that could hinder the model from good generalization. But I added the end token, because I think it is helpful for the model to know where is the end of his answer and could help him in the generalization process.

I also decided to use a right padding. That should be better for our generative model, I read that in an article and it also makes sense. A real input looks like:

> Hey, I wanted to talk to you about something.<sep>Hey, what's on your mind?<sep>I've been feeling really anxious lately.<sep>I'm sorry to hear that. Would you like to talk about it?<sep>I don't know, it just feels overwhelming.<sep>I understand. Sometimes facing our fears head-on can help. Have you ever tried any small tasks to help alleviate your anxiety?<sep>No, I haven't. What kind of tasks do you mean?<sep>Well, for example, you could try taking up a creative hobby like drawing or painting. It can be a great way to express yourself and take your mind off things.<sep>That sounds interesting. I've always wanted to learn how to draw.<sep>Great! You could start by watching some beginner tutorials online or even taking a short class. It doesn't have to be perfect, just have fun with it and let your creativity flow.<sep>I never thought of that. It could be a nice distraction from my anxiety.<bot>Exactly! Another idea is to try journaling. Writing down your thoughts and feelings can provide a sense of release and clarity.<end><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad><pad>



This will be given as input and as the target/label. The model also gets a attention mask, so that it not learns the paddings.

All training details can be found in [train.ipynb](./train.ipynb).



Duration: 

- 0 Days
- 1 Hours 
- 55 Minutes
- 43 Seconds



Loss:

<img src="loss_V_5_smoothed.png"></img>



### Second Fine-Tuning

To make the model more stable and add the chatbot more usability there was a second fine-tuning phase where the model is trained with new data (including the data from the first fine tuning).

The new data contains dialogs about visualizations and about common conversations.

The generation of the new data needed (without the original data): 

- 0 Days
- 19 Hours 
- 12 Minutes
- 1 Seconds



=> Created 4353 Training-Dialogs.



Results in 47488 (36341 new) Input-Output Pairs! (included the previous fine-tuning data).



This time I decided to increase to 8 epochs because of the higher complexity of the data.

All training details can be found in [train_refinetuning.ipynb](./train_refinetuning.ipynb).



Duration: 

- 0 Days
- 10 Hours 
- 39 Minutes
- 29 Seconds



Loss:

<img src="model_V6_loss_smoothed.png"></img>



### Hardware

**Traindata Generation**

Since I used the Openai-API as previsly described I just needed a CPU to run the loop of data generation.



**Fine-Tuning**  and **Second Fine-Tuning**

- GPU: Tesla V100-SXM2-16GB
- GPU-RAM: 16 GB
  - Usage with Batch-Size 4: 14.3 GB
  - 5.36 calculation units per hour
- CPU: Intel(R) Xeon(R) CPU @ 2.00GHz
- RAM: 12.7 GB



### Evaluation

*Have to be updated

Conversation with bad mood:

``````
...
``````



Conversation with good mood:

``````
User: Hey, how are you?
Bot: I'm doing okay, thanks for asking. How about you?
User: I feel great
Bot: Hey! You won't believe what happened to me today.
User: What? Tell me
Bot: I won a free trip to Hawaii from my friend.
User: Wow that is amzing!
Bot: That sounds amazing! How did you win it?
``````

``````
...
``````



Variaty/Eloquent:

``````
...
``````



Context:

``````
...
``````



Question-Answering:

``````
User: What is your name?
Bot: Hey, I'm John. Nice to meet you.
``````

``````
User: How hot have my water be to boil?
Bot: Hey, I'm going to give it a try. Let me know how it goes!
``````



Calculation:

``````
User: What is 1+1?
Bot: Yeah, I guess I'm right. Guess what?
``````




Translation:

...



Story creation:

...



**Result**

Is the bot working as psychologist? As friend? As sorrow talking bot?



### Result

- Building a customize GPT2-based chatbot is a suitable and cheap method
- Traindata generation with ChatGPT can be very succefull and have many advantages













