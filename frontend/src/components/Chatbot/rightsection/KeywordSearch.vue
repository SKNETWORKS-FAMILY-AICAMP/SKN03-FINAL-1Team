<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const router = useRouter()

const inputPrompt = ref('')
const generatedResults = ref(null)
const loading = ref(false) // 로딩 상태 추가
const errorMessage = ref('') // 에러 메시지 상태 추가

const showIntroAndSteps = ref(true)

const steps = [
  { id: 1, text: '키워드 변환을 통해 내가 원하는 논문 검색에 필요한 키워드를 추출하세요.' },
  { id: 2, text: '해당 키워드를 기반으로 논문을 검색하세요.' },
  { id: 3, text: '검색된 논문들을 저장하고 논문 파악을 통해 논문의 난이도를 파악하세요.' },
]

const accessToken = 'temp' // 실제 토큰을 할당

const mockResponse = {
  resultCode: 201,
  message: 'Keyword completed successfully',
  result: {
    generatedPrompt:
      '"Efficient fine-tuning strategies for large-scale pre-trained language models"의 키워드 검색 결과입니다.\n\n',
    generatedKeywordList: [
      {
        generatedKeyword:
          'Performance enhancement of pre-trained models [사전 학습된 모델의 성능 향상]',
        paperList: [
          {
            paperDoi: '10.18653/v1/2023.acl-long.437',
            title:
              'On the Evaluation of Neural Selective Prediction Methods for Natural Language Processing',
            engAbstract:
              'We provide a survey and empirical comparison of the state-of-the-art in neural selective classification for NLP tasks. We also provide a methodological blueprint, including a novel metric called refinement that provides a calibrated evaluation of confidence functions for selective prediction. Finally, we supply documented, open-source code to support the future development of selective prediction techniques.',
            citation: 0,
          },
          {
            paperDoi: '10.18653/v1/2020.acl-demos.15',
            title:
              'jiant: A Software Toolkit for Research on General-Purpose Text Understanding Models',
            engAbstract:
              'We introduce jiant, an open source toolkit for conducting multitask and transfer learning experiments on English NLU tasks. jiant enables modular and configuration driven experimentation with state-of-the-art models and a broad set of tasks for probing, transfer learning, and multitask training experiments. jiant implements over 50 NLU tasks, including all GLUE and SuperGLUE benchmark tasks. We demonstrate that jiant reproduces published performance on a variety of tasks and models, e.g., RoBERTa and BERT.',
            citation: 92,
          },
          {
            paperDoi: '10.18653/v1/2024.acl-long.726',
            title: 'Advancing Parameter Efficiency in Fine-tuning via Representation Editing',
            engAbstract:
              'Parameter Efficient Fine-Tuning (PEFT) has gained significant attention for its ability to achieve competitive results while updating only a small subset of trainable parameters. Despite the promising performance of current PEFT methods, they present challenges in hyperparameter selection, such as determining the rank of LoRA or Adapter, or specifying the length of soft prompts. In addressing these challenges, we propose a novel approach to fine-tuning neural models, termed Representation EDiting (RED), which scales and biases the representation produced at each layer. RED substantially reduces the number of trainable parameters by a factor of 25,700 compared to full parameter fine-tuning, and by a factor of 32 compared to LoRA. Remarkably, RED achieves comparable or superior results to full parameter fine-tuning and other PEFT methods. Extensive experiments were conducted across models of varying architectures and scales, including RoBERTa, GPT-2, T5, and Llama-2, and the results demonstrate the efficiency and efficacy of RED, positioning it as a promising PEFT approach for large neural models.',
            citation: 14,
          },
        ],
      },
      {
        generatedKeyword: 'Large-scale language model optimization [대규모 언어 모델 최적화]',
        paperList: [
          {
            paperDoi: '10.18653/v1/2024.acl-long.845',
            title: 'Aya Model: An Instruction Finetuned Open-Access Multilingual Language Model',
            engAbstract:
              'Recent breakthroughs in large language models (LLMs) have centered around a handful of data-rich languages. What does it take to broaden access to breakthroughs beyond first-class citizen languages? Our work introduces Aya, a massively multilingual generative language model that follows instructions in 101 languages of which over 50% are considered as lower-resourced. Aya outperforms mT0 and BLOOMZ on the majority of tasks while covering double the number of languages. We introduce extensive new evaluation suites that broaden the state-of-art for multilingual eval across 99 languages —— including discriminative and generative tasks, human evaluation, and simulated win rates that cover both held-out tasks and in-distribution performance. Furthermore, we conduct detailed investigations on the optimal finetuning mixture composition, data pruning, as well as the toxicity, bias, and safety of our models.',
            citation: 116,
          },
          {
            paperDoi: '10.18653/v1/2023.acl-tutorials.3',
            title:
              'Everything you need to know about Multilingual LLMs: Towards fair, performant and reliable models for languages of the world',
            engAbstract:
              'This tutorial will describe various aspects of scaling up language technologies to many of the world’s languages by describing the latest research in Massively Multilingual Language Models (MMLMs). We will cover topics such as data collection, training and fine-tuning of models, Responsible AI issues such as fairness, bias and toxicity, linguistic diversity and evaluation in the context of MMLMs, specifically focusing on issues in non-English and low-resource languages. Further, we will also talk about some of the real-world challenges in deploying these models in language communities in the field. With the performance of MMLMs improving in the zero-shot setting for many languages, it is now becoming feasible to use them for building language technologies in many languages of the world, and this tutorial will provide the computational linguistics community with unique insights from the latest research in multilingual models.',
            citation: 7,
          },
          {
            paperDoi: '10.18653/v1/2020.acl-main.417',
            title: 'ParaCrawl: Web-Scale Acquisition of Parallel Corpora',
            engAbstract:
              'We report on methods to create the largest publicly available parallel corpora by crawling the web, using open source software. We empirically compare alternative methods and publish benchmark data sets for sentence alignment and sentence pair filtering. We also describe the parallel corpora released and evaluate their quality and their usefulness to create machine translation systems.',
            citation: 227,
          },
        ],
      },
      {
        generatedKeyword:
          'Deep Learning model fine-tuning strategies [딥 러닝 모델 세부 조정 전략]',
        paperList: [
          {
            paperDoi: '10.18653/v1/2020.acl-demos.15',
            title:
              'jiant: A Software Toolkit for Research on General-Purpose Text Understanding Models',
            engAbstract:
              'We introduce jiant, an open source toolkit for conducting multitask and transfer learning experiments on English NLU tasks. jiant enables modular and configuration driven experimentation with state-of-the-art models and a broad set of tasks for probing, transfer learning, and multitask training experiments. jiant implements over 50 NLU tasks, including all GLUE and SuperGLUE benchmark tasks. We demonstrate that jiant reproduces published performance on a variety of tasks and models, e.g., RoBERTa and BERT.',
            citation: 92,
          },
          {
            paperDoi: '10.18653/v1/2023.acl-long.437',
            title:
              'On the Evaluation of Neural Selective Prediction Methods for Natural Language Processing',
            engAbstract:
              'We provide a survey and empirical comparison of the state-of-the-art in neural selective classification for NLP tasks. We also provide a methodological blueprint, including a novel metric called refinement that provides a calibrated evaluation of confidence functions for selective prediction. Finally, we supply documented, open-source code to support the future development of selective prediction techniques.',
            citation: 0,
          },
          {
            paperDoi: '10.18653/v1/2024.acl-long.726',
            title: 'Advancing Parameter Efficiency in Fine-tuning via Representation Editing',
            engAbstract:
              'Parameter Efficient Fine-Tuning (PEFT) has gained significant attention for its ability to achieve competitive results while updating only a small subset of trainable parameters. Despite the promising performance of current PEFT methods, they present challenges in hyperparameter selection, such as determining the rank of LoRA or Adapter, or specifying the length of soft prompts. In addressing these challenges, we propose a novel approach to fine-tuning neural models, termed Representation EDiting (RED), which scales and biases the representation produced at each layer. RED substantially reduces the number of trainable parameters by a factor of 25,700 compared to full parameter fine-tuning, and by a factor of 32 compared to LoRA. Remarkably, RED achieves comparable or superior results to full parameter fine-tuning and other PEFT methods. Extensive experiments were conducted across models of varying architectures and scales, including RoBERTa, GPT-2, T5, and Llama-2, and the results demonstrate the efficiency and efficacy of RED, positioning it as a promising PEFT approach for large neural models.',
            citation: 14,
          },
        ],
      },
      {
        generatedKeyword:
          'Advanced adaptation of pre-trained models [사전 학습된 모델의 고급 적응]',
        paperList: [
          {
            paperDoi: '10.18653/v1/2022.acl-long.264',
            title: 'The Trade-offs of Domain Adaptation for Neural Language Models',
            engAbstract:
              'This work connects language model adaptation with concepts of machine learning theory. We consider a training setup with a large out-of-domain set and a small in-domain set. We derive how the benefit of training a model on either set depends on the size of the sets and the distance between their underlying distributions. We analyze how out-of-domain pre-training before in-domain fine-tuning achieves better generalization than either solution independently. Finally, we present how adaptation techniques based on data selection, such as importance sampling, intelligent data selection and influence functions, can be presented in a common framework which highlights their similarity and also their subtle differences.',
            citation: 18,
          },
          {
            paperDoi: '10.18653/v1/2020.acl-demos.15',
            title:
              'jiant: A Software Toolkit for Research on General-Purpose Text Understanding Models',
            engAbstract:
              'We introduce jiant, an open source toolkit for conducting multitask and transfer learning experiments on English NLU tasks. jiant enables modular and configuration driven experimentation with state-of-the-art models and a broad set of tasks for probing, transfer learning, and multitask training experiments. jiant implements over 50 NLU tasks, including all GLUE and SuperGLUE benchmark tasks. We demonstrate that jiant reproduces published performance on a variety of tasks and models, e.g., RoBERTa and BERT.',
            citation: 92,
          },
          {
            paperDoi: '10.18653/v1/2022.acl-demo.26',
            title: 'Adaptor: Objective-Centric Adaptation Framework for Language Models',
            engAbstract:
              'This paper introduces Adaptor library, which transposes traditional model-centric approach composed of pre-training + fine-tuning steps to objective-centric approach, composing the training process by applications of selected objectives. We survey research directions that can benefit from enhanced objective-centric experimentation in multitask training, custom objectives development, dynamic training curricula, or domain adaptation. Adaptor aims to ease reproducibility of these research directions in practice. Finally, we demonstrate the practical applicability of Adaptor in selected unsupervised domain adaptation scenarios.',
            citation: 10,
          },
        ],
      },
    ],
  },
}

// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  showIntroAndSteps.value = false
  loading.value = true // 로딩 시작
  errorMessage.value = '' // 기존 에러 메시지 초기화
  try {
    const response = await axios.post(
      '/papers/transformation/',
      {
        userPrompt: inputPrompt.value,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`, // Authorization 헤더에 토큰 포함
        },
      },
    )
    generatedResults.value = response.data.result
    console.log('Optimized Results:', generatedResults.value)
  } catch (error) {
    if (error.response && error.response.status === 404) {
      errorMessage.value = '그런건 없어요'
    } else if (error.message && error.message.includes('CORS')) {
      errorMessage.value = 'CORS 오류가 발생했습니다. 서버 설정을 확인해주세요.'
    } else {
      console.error('키워드 최적화에 실패했습니다:', error)
      errorMessage.value = '키워드 최적화에 실패했습니다. 다시 시도해주세요.'
    }
  } finally {
    loading.value = false // 로딩 종료
  }
}

// 메시지 전송 핸들러
const handleOptimization = () => {
  if (inputPrompt.value.trim() !== '') {
    optimizeKeywords()
  } else {
    console.warn('최적화할 프롬프트를 입력해보세요.')
  }
}

// DOI 요청 핸들러 및 페이지 이동
const requestPaperByDoi = async (doi) => {
  try {
    const response = await axios.get(`/papers/select/?paperDoi=${doi}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`, // Authorization 헤더에 토큰 포함
      },
    })
    if (response.data.resultCode === 201) {
      const paperS3Path = response.data.result.paperS3Path
      router.push({
        path: '/paper/select',
        query: { paperS3Path },
      })
    }
  } catch (error) {
    console.error('논문 세부 정보를 가져오는데 실패했습니다:', error)
    errorMessage.value = '논문 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.'
  }
}
</script>

<template>
  <div class="main-container">
    <div class="test-content">
      <div class="input-area d-flex w-100 p-2">
        <input
          v-model="inputPrompt"
          type="text"
          class="form-control chat-input"
          placeholder="원하는 논문의 내용을 자신만의 언어로 표현해보세요."
          @keyup.enter="handleOptimization"
          :disabled="loading"
        />
        <button class="btn send-button" @click="handleOptimization" :disabled="loading">></button>
      </div>

      <div v-if="loading" class="d-flex justify-content-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩 중...</span>
        </div>
      </div>

      <div v-else>
        <div v-if="errorMessage" class="alert alert-danger text-center">
          {{ errorMessage }}
        </div>

        <div v-if="generatedResults" class="results-area mt-5">
          <h3 class="mb-4">최적화된 키워드 및 논문:</h3>
          <div class="mb-4">
            <h4>생성된 프롬프트: {{ generatedResults.generatedPrompt }}</h4>
          </div>
          <div
            v-for="(keywordItem, index) in generatedResults.generatedKeywordList"
            :key="index"
            class="mb-4"
          >
            <h5 class="fw-bold">키워드: {{ keywordItem.generatedKeyword }}</h5>
            <div
              v-for="(paper, paperIndex) in keywordItem.paperList"
              :key="paperIndex"
              class="card mb-3 shadow-sm"
              @click="requestPaperByDoi(paper.paperDoi)"
              style="cursor: pointer"
            >
              <div class="card-body">
                <h6>{{ paper.title }}</h6>
                <p><strong>DOI:</strong> {{ paper.paperDoi }}</p>
                <p><strong>초록:</strong> {{ paper.korAbstract }}</p>
                <p><strong>인용 수:</strong> {{ paper.citation }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="showIntroAndSteps" class="intro-text text-center mb-4">
          <p class="text-muted">논문 검색이 어려우신가요? <br /></p>
          <p class="text-muted">
            도큐멘토와 함께 검색 키워드를 정의하고, <br />
            읽어야 할, 읽을 수 있는 논문을 탐색해보아요!
          </p>
        </div>
      </div>
      <div v-if="showIntroAndSteps" class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded shadow text-center m-2"
            v-for="step in steps"
            :key="step.id"
            style="flex: 1"
          >
            <h5>Step {{ step.id }}</h5>
            <p>{{ step.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  width: 600px;
}

.test-content {
  width: 600px;
}

.input-area {
  border: 1px solid #a04747;
  border-radius: 50px;
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}

.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: none;
}

.chat-input:focus {
  border-color: none;
  box-shadow: none;
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.send-button:hover {
  background-color: #7a3737; /* 어두운 빨간색으로 변경 */
}

.results-area .card {
  max-width: 600px;
  margin: 0 auto;
}

.intro-text {
  margin-top: 20px;
}

/* steps 관련 스타일 */
.steps-container {
  margin-top: 50px;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.shadow {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
