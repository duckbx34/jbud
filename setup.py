from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jbud",
    version="1.0.0",
    author="JBUD Contributors",
    description="Local Personal Journal AI - Completely private journaling with AI insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jbud",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "langchain>=0.1.0",
        "chromadb>=0.4.0",
        "ollama>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "jbud=jbud:main",
        ],
    },
)