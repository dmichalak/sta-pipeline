from setuptools import setup, find_packages

setup(
    name="sta_pipeline",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "click",
        "mrcfile",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "sta_alignframes=src.preprocessing.sta_alignframes:cli",
            "sta_alignframes_multiprocessing=src.preprocessing.sta_alignframes_multiprocessing:cli",
            "sta_batchruntomo=src.preprocessing.sta_batchruntomo:cli",
            "sta_ctfplotter=src.preprocessing.sta_ctfplotter:cli",
            "sta_fidder=src.preprocessing.sta_fidder:cli",
            "sta_rescale_tiltstack=src.preprocessing.sta_rescale_tiltstack:cli",
            "sta_defoci=src.isonet.sta_defoci:cli",
            "sta_isonet=src.isonet.sta_isonet:cli",
            
            "sta_eman2=src.eman2.sta_eman2:cli",
        ]
    },
)
