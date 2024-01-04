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

To contain the context it was important to add the context of the conversation to the input prompt. It is questionable how good this works. Currently it's not sure how many messages are given by the given 1024 tokens. Also it's not clear, if the user and bot inputs markings are working like I wish (I added marks to it <start_user>...<end_user><start_bot>...). And finally it could happen, that messages are splitted somewhere and the context could propably change through this process.

I expect that a low epoch-rate will be fine, because the data is partwise very similiar, so in one epoch the model saw the same data more than one times, I don't know how often exactly. 

The Batch-Size is 4, which is very small, but my available GPU-RAM had no more capacity.









