# AI Sound Classification for Early Detection of Childhood Stuttering

Code for my UTS Honours thesis. Three classifiers (static MFCC + Random Forest, DTW + Random Forest, fine-tuned Wav2Vec 2.0) are trained on SEP-28k-E and evaluated on the SEP-28k-E test split and on UCLASS (child vs adult speakers).

Forked from [SEP-28k-Extended](https://github.com/th-nuernberg/ml-stuttering-events-dataset-extended) (Bayerl et al., 2022), which extends Apple's [SEP-28k](https://github.com/apple/ml-stuttering-events-dataset) (Lea et al., 2021).

## Usage

```
pip install -r requirements.txt
python download_audio.py --episodes SEP-28k-Extended_episodes.csv --wavs wavs
```

Download the SEP-28k-formatted UCLASS clips from [Kaggle](https://www.kaggle.com/datasets/vudominhgiang/uclass-stuttered-speech-clips-sep-28k-format), then run the notebooks in order:

1. `dataset_download_audit.ipynb`
2. `UCLASS_Preprocessing.ipynb`
3. `Model.ipynb`
4. `Model2_DTW_RF.ipynb`
5. `Model1_Wav2Vec2.ipynb`
6. `Results_Summary.ipynb`

## License

Code: see [LICENSE](LICENSE). SEP-28k-E data: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Podcast audio copyright remains with the podcast owners.
