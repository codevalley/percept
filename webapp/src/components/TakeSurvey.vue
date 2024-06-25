<template>
    <div class="take-survey">
      <h2>{{ currentQuestion.text }}</h2>
      <div class="answer-options">
        <button 
          v-for="n in 10" 
          :key="n" 
          @click="selectAnswer(n)"
          :class="['option', { selected: currentAnswer === n }]"
        >
          {{ n }}
        </button>
      </div>
      <div class="progress-bar">
        <div class="progress" :style="{ width: `${progress}%` }"></div>
      </div>
      <button @click="nextQuestion" class="btn" :disabled="!currentAnswer">Next</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TakeSurvey',
    props: ['surveyCode'],
    data() {
      return {
        questions: [
          { id: 1, text: "How likely are you to recommend our company to a friend or colleague?" },
          { id: 2, text: "How satisfied are you with our product?" },
          // Add more questions as needed
        ],
        currentQuestionIndex: 0,
        answers: {},
        currentAnswer: null
      }
    },
    computed: {
      currentQuestion() {
        return this.questions[this.currentQuestionIndex];
      },
      progress() {
        return ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
      }
    },
    methods: {
      selectAnswer(value) {
        this.currentAnswer = value;
      },
      nextQuestion() {
        this.answers[this.currentQuestion.id] = this.currentAnswer;
        this.currentAnswer = null;
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++;
        } else {
          // Survey completed, handle submission
          console.log('Survey completed', this.answers);
          // Here you would typically send the answers to your backend
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .answer-options {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
  }
  
  .option {
    width: 40px;
    height: 40px;
    border: 1px solid #ccc;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .option.selected {
    background-color: #3498db;
    color: white;
  }
  
  .progress-bar {
    width: 100%;
    height: 10px;
    background-color: #eee;
    border-radius: 5px;
    margin-bottom: 20px;
  }
  
  .progress {
    height: 100%;
    background-color: #3498db;
    border-radius: 5px;
    transition: width 0.3s ease-in-out;
  }
  
  .btn {
    padding: 10px 20px;
    font-size: 18px;
    border: none;
    border-radius: 25px;
    background-color: #3498db;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .btn:hover:not(:disabled) {
    background-color: #2980b9;
  }
  </style>