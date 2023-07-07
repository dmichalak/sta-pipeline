from setuptools import setup, find_packages

setup(
    name="sta_pipeline",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "click",
        "pandas",
        "mrcfile",
        "starfile",
    ],
    entry_points={
        "console_scripts": [
            "sta_alignframes=src.sta_pipeline.preprocessing.sta_alignframes:cli",
            "sta_alignframes_multiprocessing=src.sta_pipeline.preprocessing.sta_alignframes_multiprocessing:cli",
            "sta_batchruntomo=src.sta_pipeline.preprocessing.sta_batchruntomo:cli",
            "sta_ctfplotter=src.sta_pipeline.preprocessing.sta_ctfplotter:cli",
            "sta_fidder=src.sta_pipeline.preprocessing.sta_fidder:cli",
            "sta_rescale_tiltstack=src.sta_pipeline.preprocessing.sta_rescale_tiltstack:cli",
            "sta_defoci=src.sta_pipeline.isonet.sta_defoci:cli",
            "sta_isonet=src.sta_pipeline.isonet.sta_isonet:cli",
            #"sta_viewmask=src.sta_pipeline.isonet.sta_viewmask:cli",
            "sta_eman2=src.sta_pipeline.eman2.sta_eman2:cli",
        ]
    },
)
