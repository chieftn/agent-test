import asyncio
# import mistune # import HTMLRenderer, create_markdown, html
#from bs4 import BeautifulSoup
#import marko
import toml

# class CustomRenderer(HTMLRenderer):
#     def heading(self, text, level):
#         print('hello')
#         return f'<h{level} class="custom-heading">{text}</h{level}>\n'

async def main():
    # file1 = open("./artifacts/myTest.md","r")
    # file1_content = file1.read()

    with open('./artifacts/myTest.toml', 'r') as f:
        config = toml.load(f)

    # print(config['describe']['block'])
    print(config['describe'][0]['it'])

    # print(marko.convert(file1_content))

    #me = mistune.html(file1_content)

    #soup = BeautifulSoup(me, 'html.parser')
    #print(soup.p)
    # data = pypandoc.convert_file('./artifacts/myTest.md', 'json')
    #data = pypandoc.convert_text(file1_content, "json")
    #print(data)


    #file1_parse = create_markdown(file1_content, renderer=CustomRenderer)
    #print(file1_parse)


asyncio.run(main())