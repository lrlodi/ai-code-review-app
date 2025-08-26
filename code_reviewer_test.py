import pytest
from unittest.mock import patch, MagicMock
from CodeReviewer import CodeReviewer

@pytest.fixture
def reviewer():
    return CodeReviewer()

def test_format_prompt_python(reviewer):
    code = "def hello(): print('hi')"
    prompt = reviewer.format_prompt(code, "Python", "Supportive")
    assert "You are an expert Python reviewer." in prompt
    assert "Use a Supportive tone:" in prompt
    assert "def hello()" in prompt

def test_format_prompt_php(reviewer):
    code = "public function hello(){ return 'hi}'"
    prompt = reviewer.format_prompt(code, "PHP", "Humorous")
    assert "You are an expert PHP reviewer." in prompt
    assert "Use a Humorous tone:" in prompt
    assert "public function hello()" in prompt

def test_format_prompt_javascript(reviewer):
    code = "function hello(){ return 'hi}'"
    prompt = reviewer.format_prompt(code, "Javascript", "Direct")
    assert "You are an expert Javascript reviewer." in prompt
    assert "Use a Direct tone:" in prompt
    assert "function hello()" in prompt

def test_format_prompt_java(reviewer):
    code = "public class Hello { static void hello() { System.out.println('hi')} }"
    prompt = reviewer.format_prompt(code, "Java", "Direct")
    assert "You are an expert Java reviewer." in prompt
    assert "Use a Direct tone:" in prompt
    assert "public class Hello" in prompt

def test_format_prompt_c(reviewer):
    code = "str hello() { return 'hi' }"
    prompt = reviewer.format_prompt(code, "C", "Supportive")
    assert "You are an expert C reviewer." in prompt
    assert "Use a Supportive tone:" in prompt
    assert "str hello" in prompt

def test_format_prompt_c_sharp(reviewer):
    code = "str hello() { return 'hi' }"
    prompt = reviewer.format_prompt(code, "C#", "Supportive")
    assert "You are an expert C# reviewer." in prompt
    assert "Use a Supportive tone:" in prompt
    assert "str hello" in prompt

@patch("openai.ChatCompletion.create")
def test_get_code_feedback(mock_create, reviewer):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message={"content": "Some code review details"})]
    mock_response.usage = MagicMock(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    mock_create.return_value = mock_response

    code = "def hello(): print('hi')"
    result = reviewer.get_code_feedback(code, "Python", "Supportive")

    assert result["feedback"] == "Some code review details"
    assert result["tokens_prompt"] == 10
    assert result["tokens_completion"] == 20
    assert result["tokens_total"] == 30
