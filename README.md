<h1 style="text-align:center">Rest in Story 🐘</h1>

<h2 style="text-align:center">RIS-Bot</h2>

<h3 style="text-align:center">Your Story to calm 🏖️</h3>

<!--Your interactive story companion for serene moments-->
<!--Experience pure calmness-->
<!--The bot you wish was your therapist🏖️-->

> Important disclaimer: This is only a small project and the bot doesn't replace serious help, but it can help you.



Tags: 
- chatbot
- english
- GPT2
- anxiety/stress/....

<br><br>

### Guide

...



### Description

A GPT2 model is to be extended to a new task via transfer learning. The GPT2 model is to be fine-tuned in such a way that it generates interactive, meditative and calming stories for the user and goes through them with them.<br>
The communication participant should be positively encouraged and reassured.<br>
The aim is to create a reading experience that promotes positive thoughts.<br>
The language is English and the model is to be deployed on Discord.<br>
Interaction data from a user and a storyteller is required for the training data.<br>
Since such training data is difficult to obtain, ChatGPT is used to generate the data.<br>

The GPT3 model would actually be used for this, but this is associated with costs, so the decision was made to use the GPT2 model.




### Project Milestones:
- Traindata Commands are implemented
- Traindata (dialogs) with ChatGPT are generated
- A GPT2 model was trained/finetuned with the training data
- The bot got deployed on Discord over replit



### Advantages and Disadvantages

Pros:

- for free
- every time
- everywhere 
- 100% private 
- your unique story



Cons:

- May not answer well every time
- Can the bot learn it?
- Stories may not be creative enough? 



### Branches

- main = contains the trained model and scripts to train the model
- every other branch is a platform integration (Discord, Mobile, Desktop,...)



### Procedure:

<!--

First message from "User" -> will be given from the system:
Tell me an interactive story to calm me down. It should be mindful with lots of details and meditative. Breathing exercises and visualizations should also be incorporated into the story.-->

1. The system writes a welcome message and that the user should write down 3 words or "surprise me"/"you decide"/"".
2. Then the user writes 3 words or "surprise me"/"you decide"/"". Which is the first Input for the GPT-Model
3. The algorithm uses the 3 words to create a calm story or generates a own story, when no word is given (or the user wants the system to surprise him)
4. Now the User should have an interactive story to calm down



### Fine-Tuning Data

For the data I use ChatGPT to generate my data. Therefore I need to prepare different commands to get the data. Also I have to program which picks different commands and calls ChatGPT over API.



Commands:

- ...



Different Scenarios:

- ...
