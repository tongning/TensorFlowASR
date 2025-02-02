# Copyright 2020 Huy Le Nguyen (@usimarit)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse
from tensorflow_asr.configs.config import Config
from tensorflow_asr.utils.utils import preprocess_paths
from tensorflow_asr.datasets.asr_dataset import ASRTFRecordDataset
from tensorflow_asr.featurizers.text_featurizers import SubwordFeaturizer, SentencePieceFeaturizer, CharFeaturizer

parser = argparse.ArgumentParser(prog="TFRecords Creation")

parser.add_argument("--mode", "-m", type=str, default=None, help="Mode")

parser.add_argument("--config", type=str, default=None, help="The file path of model configuration file")

parser.add_argument("--tfrecords_dir", type=str, default=None, help="Directory to tfrecords")

parser.add_argument("--tfrecords_shards", type=int, default=16, help="Number of tfrecords shards")

parser.add_argument("--shuffle", default=False, action="store_true", help="Shuffle data or not")

parser.add_argument("--sentence_piece", default=False, action="store_true", help="Whether to use `SentencePiece` model")

parser.add_argument("--subwords", type=str, default=None, help="Path to file that stores generated subwords")

parser.add_argument("transcripts", nargs="+", type=str, default=None, help="Paths to transcript files")

args = parser.parse_args()

transcripts = preprocess_paths(args.transcripts)
tfrecords_dir = preprocess_paths(args.tfrecords_dir)

config = Config(args.config)

if args.sentence_piece:
    print("Loading SentencePiece model ...")
    text_featurizer = SentencePieceFeaturizer.load_from_file(config.decoder_config, args.subwords)
elif args.subwords and os.path.exists(args.subwords):
    print("Loading subwords ...")
    text_featurizer = SubwordFeaturizer.load_from_file(config.decoder_config, args.subwords)
else:
    print("Using character featurizer ...")
    text_featurizer = CharFeaturizer(config.decoder_config)

ASRTFRecordDataset(
    data_paths=transcripts, tfrecords_dir=tfrecords_dir,
    speech_featurizer=None, text_featurizer=text_featurizer,
    stage=args.mode, shuffle=args.shuffle, tfrecords_shards=args.tfrecords_shards
).create_tfrecords()
