import torch as th
import transformers
from typing import List


def get_sentence_embed(
    sents: List[str],
    model: transformers.BertModel,
    tokenizer: transformers.BertTokenizer,
) -> th.Tensor:
    """
    Get the sentence embeddings of the given list sentences.
    ---
    Parameters:
    ---
    sents (List[str]): The list of sentences.
    model (transformers.BertModel): The BERT model.
    tokenizer (transformers.BertTokenizer): The BERT tokenizer.
    """
    encoded_sent = th.concat(
        [tokenizer.encode(sent, return_tensors="pt") for sent in sents]
    )
    with th.no_grad():
        output = model(encoded_sent)
    return output[1]
