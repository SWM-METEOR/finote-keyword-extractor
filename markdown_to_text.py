from bs4 import BeautifulSoup
import markdown2
import re
import body_request


def markdown_to_text(bodyRequest: body_request.BodyRequest):
    # Markdown 문자열을 HTML로 파싱
    markdown_string = bodyRequest.bodyString
    html_content = markdown2.markdown(markdown_string)

    # BeautifulSoup을 사용하여 HTML 태그 제거
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()

    # 코드블럭 제거
    code_block_pattern = re.compile(r'```.*?```', re.DOTALL)

    text_content = re.sub(code_block_pattern, '', text_content)

    # 빈 줄 제거
    text_content = "\n".join([line for line in text_content.splitlines() if line.strip()])

    return text_content
