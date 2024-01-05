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
- [Guide](#guide)
- [Branches](#branches)
- [Fine-Tuning](#fine-tuning)



### Tags

- chatbot
- english
- GPT2
- anxiety/stress/....



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

<br>

### Definition Talk Down
A "talk down" for anxiety usually refers to a technique used in cognitive behavioral therapy. It is a type of self-talk in which you make reassuring and rational statements to yourself in order to reduce the intensity of your anxiety. <br>
A "talk down" for anxiety involves several key attributes: <br>
1. self-soothing: You make soothing statements to yourself to reduce the intensity of the anxiety. This can include things like "I'm safe" or "This is only temporary".

2. rational thoughts: You try to replace the irrational fears you have with rational and logical thoughts. For example, you could say to yourself: "There is no real reason for this fear".

3. mindfulness: focus on the here and now instead of focusing on the future or the past. This can help to reduce anxiety by focusing on what is happening right now rather than what might happen.

4. relaxation techniques: Techniques such as deep breathing or progressive muscle relaxation can help to alleviate the physical symptoms of anxiety.




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



### Guide

...



### Branches

- main = contains the trained model and scripts to train the model
- every other branch is a platform integration (Discord, Mobile, Desktop,...)





### Fine-Tuning

For the fine-tuning there are many things to respect. Here the most important facts. I used the Google Collab environment with the NVIDIA Tesla V100.

For the optimizer I orintated on models like GPT-3 and used the Adam-Optimizer. And I choose a small learnrate 1*e-4 to genralise well.

To contain the context it was important to add the context of the conversation to the input prompt. It is questionable how good this works. Currently it's not sure how many messages are given by the given 1024 tokens. Also it's not clear, if the user and bot inputs markings are working like I wish (I added marks to itlike: ...\<sep>... -> see below for a indeepth example). And finally it could happen, that messages are splitted somewhere and the context could propably change through this process. Also the missing of start and/or end token can hinder the model, but I expect this is not a problem, since the provided informations of these tokens are not so important (from my perspective). 

I expect that a low epoch-rate will be fine, because the data is partwise very similiar, so in one epoch the model saw the same data more than one times, I don't know how often exactly. 

The Batch-Size is 4, which is very small, but my available GPU-RAM had no more capacity.

In a [Kaggle tutorial](https://www.kaggle.com/code/pinooxd/gpt2-chatbot/notebook#PS) the author created train data like following:

> no puedo.<|endoftext|>¡Espera!<|endoftext|>¡Espera!<|endoftext|>No me acompañes.<|endoftext|>¡Con cuidado, te puedes golpear la pierna!<|endoftext|>En el frente será más difícil.<|endoftext|>No te dejarán ir al frente.<|endoftext|>Sólo uno de nosotros irá al ejército, tu o yo.<|endoftext|>Tu te quedarás, por tus conocimientos y experiencias...<|endoftext|>Pero, tu tienes talento.<|endoftext|>Cuida los planos.<|endoftext|>Mi esposa me cosió...<|endoftext|>

Translated:

> Ich kann nicht.<|endoftext|>Warte!<|endoftext|>Warte!<|endoftext|>Komm nicht mit.<|endoftext|>Seien Sie vorsichtig, Sie könnten sich das Bein stoßen!<|endoftext|> An der Front wird es schwieriger.<|endoftext|>Sie werden dich nicht an die Front gehen lassen.<|endoftext|>Nur einer von uns wird zur Armee gehen, du oder ich.<|endoftext|>Du wirst bleiben , aufgrund deines Wissens und deiner Erfahrungen.. .<|endoftext|>Aber du hast Talent.<|endoftext|>Kümmere dich um die Pläne.<|endoftext|>Meine Frau hat mich genäht...<|endoftext|>



Means: We only need 1 special token \<end>  and the marking which one is saying seems to be not relevant. Also interesting is, that the label is equal the input.



Tokens as described in the [documentation](https://huggingface.co/transformers/v3.0.2/main_classes/tokenizer.html):

**bos_token** (*-*) – (Optional) string: a beginning of sentence token. Will be associated to `self.bos_token` and `self.bos_token_id`

**eos_token** (*-*) – (Optional) string: an end of sentence token. Will be associated to `self.eos_token` and `self.eos_token_id`

**sep_token** (*-*) – (Optional) string: a separation token (e.g. to separate context and query in an input sequence). Will be associated to `self.sep_token` and `self.sep_token_id`

**pad_token** (*-*) – (Optional) string: a padding token. Will be associated to `self.pad_token` and `self.pad_token_id`



Our Input with context will looks like:

> Hey, I've been feeling really down lately. I just can't seem to find any motivation or purpose in my life.**<sep>**I completely understand how you feel. I went through a similar phase a while back. I had lost all sense of direction and felt like my life lacked purpose. But then I came across this incredible story that really inspired me.**<sep>**What was the story about?**<sep>**It was about a man named Nick Vujicic. He was born without arms and legs, and faced numerous challenges and obstacles throughout his life. Despite all that, he never let his disabilities define him. Instead, he used his setbacks as fuel to achieve incredible things. He became a motivational speaker, inspiring millions of people around the world.**<sep>**That's really inspiring. But how did he manage to find motivation and purpose in his life?**<sep>**Well, Nick didn't let his circumstances determine his happiness or success. He believed that true happiness and purpose come from within, and he focused on developing a positive mindset. He found joy in helping others and making a difference in their lives. He embraced his unique situation and used it as a platform to inspire others.**<sep>**That's amazing. But I still struggle to find that inner motivation and purpose in my own life.**<bot>**I think the key is to start small and take little steps towards finding what truly makes you happy. Explore different interests, set goals for yourself, and surround yourself with positive and supportive people. Remember, everyone's journey is different, and it's okay to take your time to discover your passion and purpose. Believe in yourself and your abilities, and never give up.



> Hey, I've been feeling really overwhelmed lately and I think I might have Separation Anxiety Disorder.**<bot>**Oh, I'm sorry to hear that. What exactly are you experiencing?



I decided to only use the sep, pad and a special bot token. The sep-token will help the model to understand the context, the pad token for the padding (because the input need the same length). There is also a special bot token that allows the model to know which part is his part and can learn it.

The start token is not used, because it will be cutted away when the input is too big and that could hinder the model from good generalization. And without start token I decided also too miss the end token. In my understanding this is not important. Only to ignore the pad-tokens it could be helpful, but it depends on the exact implementation from the transformers module.







