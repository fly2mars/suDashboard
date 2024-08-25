# Copyright (c) 2024 [fly2mars@gmail.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module implements the [BaseAgent] for the suKBAgent library.

suKBAgent framework：
1. BaseAgent：Base class for BDI (Belief-Desire-) agent。
2. LLMAgent：LLM Agent, support OpenAI API compatible large language models。
3. SearchAgent：Search agent, support google searching, return related url and content list.
4. RAGAgent：使用搜索返回信息，结合用户查询结果，通过大语言模型得到最终答案。
5. ScheduleAgent：任务管理Agent，根据用户输入，组织工作流程，分别调用各个Agent完成信息录入，判断、搜索、整理和输出的人维护。
"""
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod


# A BDI Agent base class
class BaseAgent(ABC):
    def __init__(self):
        self.beliefs = {}
        self.desires = set()
        self.intentions = []

    def update_belief(self, key, value):
        self.beliefs[key] = value

    def add_desire(self, desire):
        if desire not in self.desires:
            self.desires.add(desire)

    def remove_desire(self, desire):
        if desire in self.desires:
            self.desires.discard(desire)

    @abstractmethod
    def form_intentions(self):
        pass

    @abstractmethod
    def execute_intentions(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        :param args:  commonly are input_query, context .
        :param kwargs: commonly is empty, for extension.
        :return: search answer
        """
        pass


if __name__ == "__main__":
    # Test baseAgent, this test can be found in {package_root/test/} too.
    class SimpleAgent(BaseAgent):
        def form_intentions(self):
            self.intentions = ['simple_intention']

        def execute_intentions(self):
            if 'simple_intention' in self.intentions:
                return "Executed simple intention"

        def run(self):
            self.form_intentions()
            return self.execute_intentions()

    agent = SimpleAgent()
    agent.update_belief('key', 'value')
    agent.add_desire('new_desire')
    result = agent.run()

    print("Beliefs:", agent.beliefs)
    print("Desires:", agent.desires)
    print("Run result:", result)

