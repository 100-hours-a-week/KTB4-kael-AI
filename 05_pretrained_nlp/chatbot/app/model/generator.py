"""KoGPT2 기반 autoregressive 문장 생성 모듈.

과제 핵심:
  - predict_next_token : 입력 문장의 '다음 토큰 1개'를 예측 (요건 1)
  - generate          : predict_next_token을 EOS/최대길이까지 반복 (요건 2, autoregressive)

모델은 모듈이 처음 import 될 때 1회만 메모리에 올린다(전역 싱글톤). GPU 없이 CPU로 추론한다.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

_MODEL_NAME = "skt/kogpt2-base-v2"

# 토크나이저/모델 로드 (최초 실행 시 ~500MB 자동 다운로드)
tokenizer = AutoTokenizer.from_pretrained(
    _MODEL_NAME,
    bos_token="</s>",
    eos_token="</s>",
    unk_token="<unk>",
    pad_token="<pad>",
    mask_token="<mask>",
)
model = AutoModelForCausalLM.from_pretrained(_MODEL_NAME)
model.eval()  # 추론 모드 (드롭아웃 등 비활성화)


def predict_next_token(input_ids: torch.Tensor, temperature: float, top_k: int) -> torch.Tensor:
    """요건 1: 다음 토큰 1개를 예측한다.

    흐름: 모델 forward → 마지막 위치 logits → temperature 조절 → top-k 샘플링.
    """
    with torch.no_grad():
        # logits: (batch, seq_len, vocab) → 마지막 토큰 위치만 사용
        logits = model(input_ids).logits[:, -1, :]

    # temperature: 작을수록 보수적(확신), 클수록 다양
    logits = logits / temperature

    # top-k: 확률 상위 k개 토큰만 후보로 남겨 샘플링
    top_vals, top_idx = torch.topk(logits, top_k)
    probs = torch.softmax(top_vals, dim=-1)
    sampled = torch.multinomial(probs, num_samples=1)[0]  # 후보 중 하나 선택
    return top_idx[0, sampled]


def generate(
    prompt: str,
    max_new_tokens: int = 40,
    temperature: float = 0.8,
    top_k: int = 50,
) -> str:
    """요건 2: predict_next_token을 재귀 반복(autoregressive)하여 문장을 완성한다.

    토큰을 하나 생성할 때마다 입력에 이어붙여 다시 모델에 넣는다.
    EOS 토큰이 나오거나 max_new_tokens에 도달하면 멈춘다.
    """
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    prompt_len = input_ids.shape[1]  # 생성분만 따로 디코딩하기 위한 기준

    for _ in range(max_new_tokens):
        next_id = predict_next_token(input_ids, temperature, top_k)
        if next_id.item() == tokenizer.eos_token_id:
            break
        # 생성한 토큰을 입력 뒤에 이어붙임 → 다음 스텝의 입력이 됨
        input_ids = torch.cat([input_ids, next_id.view(1, 1)], dim=-1)

    full_text = tokenizer.decode(input_ids[0], skip_special_tokens=True)
    generated_only = tokenizer.decode(input_ids[0, prompt_len:], skip_special_tokens=True)
    return full_text, generated_only


def next_word(prompt: str, temperature: float = 0.8, top_k: int = 50) -> str:
    """요건 1 시연용: 입력 문장 다음에 올 토큰(단어 조각) 1개를 문자열로 반환."""
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    next_id = predict_next_token(input_ids, temperature, top_k)
    return tokenizer.decode([next_id.item()], skip_special_tokens=True)
