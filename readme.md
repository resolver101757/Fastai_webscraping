# overview of the project

The aim is to sumarise all the blog posts from fast.ai to quickly understand what people have been writing about and to get a quick overview of the content.  We will use GPT 4 with some prompting to help this.


# how to run the project

- clone the repo
- install the requirements
- add any blogs to list_of_blogs.txt
- run the script `python3 main.py`
- the output will be in the output folder


to do 

- Write a prompt to get the data formatted correctly for the gpt4 (use chatgpt to test out the prompts)
- write a function to call the openai api
- work out how to crawl discord and forums to search for blogs and add them to the list_of_blogs.txt
- calculate the cost of api calls and how to reduce the cost

# prompt ideas 

## Fast ai prompt for insperation - taken from the fast ai website

(The “topics covered” list was taken from the concatenation of the topic list of each lesson, and using GPT 4 with this prompt: “The input text contains a markdown list of topics discussed in a number of deep learning and stable diffusion lessons. The topics from each lesson were concatenated together into this list, therefore it may contain duplicates (or near dupes) and is not well organised. Create an organised markdown list which groups similar topics together (using a hierarchy or markdown list items as appropriate) and combine duplicate or very similar topics.” The “content summary” section was taken from the “topics covered” list, and the GPT 4 prompt “Summarise the following markdown course outline using 3-4 paragraphs of informal prose in the style of Jeremy Howard. Do not follow the same order as the topics in the outline, but instead arrange them such that the most foundational and key topics come first.”)

## Prompt for structuring data

Im getting some good summaries but probably need more sturcture.

- The blogs are related to the study of deep learning and the aim is to organize and summarize each page.  
- The input contains just text.  
- The output will be organized in markdown format.
- Summarize who the blog was written about and what they are about.
- Each blog will start with ***URL: {url} *** where {url} is the name of the blog.  
- For each url write the url as their title along with description and a short description of what the aim was, overview and tools used and the findings.
- If the blog is empty or the page can not be found, dont include it in the output.

The text is following now :

- some prompts to try and sumarise the information before sending to chat gpt :  https://chat.openai.com/c/bc0dace0-1851-4525-9445-a2c435aff959