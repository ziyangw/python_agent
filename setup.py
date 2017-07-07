from setuptools import setup

setup(name='python_agent',
      version='0.3',
      description='Python Agent created by Ziyang and Vinai',
      url='https://github.com/ziyangw/python_agent',
      author=['Vinai Rachakonda', 'Ziyang Wang'],
      author_email=['rachakondavinai@gmail.com', 'ziyang.wang123@gmail.com'],
      license='MIT',
      packages=['python_agent', 'python_agent/agent', 'python_agent/analysis'],
      install_requires=[
          'webob',
          'memory_profiler',
          'psutil',
          'matplotlib',
          'beautifulsoup4'
      ],
      zip_safe=False)
