from setuptools import setup, find_packages

setup(
    name = "sta_pipeline",
    version = "0.1",
    packages = find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts" : [
            "sta_alignframes=scripts.preprocessing.run_alignframes:cli",
            "sta_batchruntomo=scripts.preprocessing.run_batchruntomo:cli",
        ]
    }
    )
