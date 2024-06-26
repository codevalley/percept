<template>
  <div class="create">
    <h2>{{ creationStage === 'questions' ? 'Create a New Survey' : 'Complete Your Survey' }}</h2>
    
    <!-- Question Creation Stage -->
    <div v-if="creationStage === 'questions'" class="question-creation">
      <div class="input-row">
        <input v-model="newQuestion.text" type="text" placeholder="Enter your question" required>
      </div>
      <div class="input-row">
        <select v-model="newQuestion.response_type" required>
          <option value="scale">Scale</option>
          <option value="boolean">Yes/No</option>
        </select>
        <input v-if="newQuestion.response_type === 'scale'" v-model.number="newQuestion.response_scale_max" type="number" min="2" max="10" placeholder="Max scale value" required>
      </div>
      <div class="input-row">
        <button @click="addQuestion" class="btn">Add Question</button>
        <button @click="startSurveyCompletion" class="btn" :disabled="questions.length === 0">Finish</button>
      </div>
    </div>

    <ul class="question-list">
      <li v-for="(question, index) in questions" :key="question.id" class="question-item">
        <div class="question-content">
          <div class="question-header">
            <span class="question-text">{{ question.text }}</span>
            <span class="question-type" :class="question.response_type">
              {{ question.response_type === 'scale' ? `Scale (1-${question.response_scale_max})` : 'Yes/No' }}
            </span>
          </div>
          
          <!-- Creator Answer Section -->
          <div v-if="creationStage === 'completion'" class="creator-answer">
            <div v-if="question.response_type === 'scale'" class="scale-answers">
              <button 
                v-for="n in question.response_scale_max" 
                :key="n" 
                @click="selectAnswer(index, n)"
                :class="['answer-btn', { selected: creatorAnswers[index] === n }]"
                :disabled="isSubmitted"
              >
                {{ n }}
              </button>
            </div>
            <div v-else class="boolean-answers">
              <button @click="selectAnswer(index, true)" :class="['answer-btn', { selected: creatorAnswers[index] === true }]" :disabled="isSubmitted">Yes</button>
              <button @click="selectAnswer(index, false)" :class="['answer-btn', { selected: creatorAnswers[index] === false }]" :disabled="isSubmitted">No</button>
            </div>
          </div>
        </div>
      </li>
    </ul>

    <!-- Submit Survey Button -->
    <button v-if="creationStage === 'completion' && !showSuccess" @click="finishSurvey" class="btn" :disabled="!allQuestionsAnswered || isLoading || isSubmitted">
      <span v-if="!isLoading">Submit Survey</span>
      <span v-else class="loader"></span>
    </button>

    <div v-if="showSuccess" class="success-message">
      <h3>Survey Created Successfully!</h3>
      <p>Survey ID: {{ createdSurveyId }}</p>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from '@/services/api';
import confetti from 'canvas-confetti';

export default {
  name: 'CreateView',
  data() {
    return {
      creationStage: 'questions',
      newQuestion: {
        text: '',
        response_type: 'scale',
        response_scale_max: 5
      },
      questions: [],
      creatorAnswers: [],
      isLoading: false,
      showSuccess: false,
      createdSurveyId: null,
      errorMessage: '',
      isSubmitted: false
    }
  },
  computed: {
    allQuestionsAnswered() {
      return this.creatorAnswers.length === this.questions.length &&
             this.creatorAnswers.every(answer => answer !== null && answer !== undefined);
    }
  },
  methods: {
    addQuestion() {
      const question = {
        id: Date.now(),
        text: this.newQuestion.text,
        response_type: this.newQuestion.response_type,
        response_scale_max: this.newQuestion.response_type === 'scale' ? this.newQuestion.response_scale_max : undefined
      };
      this.questions.push(question);
      this.newQuestion.text = '';
      this.newQuestion.response_type = 'scale';
      this.newQuestion.response_scale_max = 5;
    },
    startSurveyCompletion() {
      this.creationStage = 'completion';
      this.creatorAnswers = new Array(this.questions.length).fill(null);
    },
    selectAnswer(index, value) {
      if (!this.isSubmitted) {
        this.creatorAnswers[index] = value;
      }
    },
    async finishSurvey() {
      if (this.isSubmitted) return;
      
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const surveyData = {
          title: "New Survey",
          description: "Survey created via Backfeed",
          questions: this.questions.map((q, index) => ({
            ...q,
            creator_answer: this.creatorAnswers[index]
          }))
        };
        const response = await api.createSurvey(surveyData);
        console.log('Survey created', response.data);
        this.createdSurveyId = response.data.survey_id;
        this.showSuccess = true;
        this.isSubmitted = true;
        this.celebrateSuccess();
      } catch (error) {
        console.error('Error creating survey:', error);
        this.errorMessage = 'Error creating survey. Please try again.' + error;
      } finally {
        this.isLoading = false;
      }
    },
    celebrateSuccess() {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  }
}
</script>

<style scoped>
.create {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.question-creation {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.input-row {
  display: flex;
  gap: 10px;
}

input, select {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  flex: 1;
  padding: 10px 20px;
  font-size: 18px;
  border: none;
  border-radius: 25px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.question-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

.question-item {
  margin-bottom: 20px;
}

.question-content {
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f8f8f8;
}

.question-text {
  font-weight: bold;
}

.question-type {
  font-size: 0.8em;
  padding: 3px 8px;
  border-radius: 12px;
}

.question-type.scale {
  background-color: #e1f5fe;
  color: #0277bd;
}

.question-type.boolean {
  background-color: #f1f8e9;
  color: #558b2f;
}

.creator-answer {
  padding: 10px;
  background-color: #ffffff;
}

.scale-answers, .boolean-answers {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.answer-btn {
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #e0e0e0;
  background-color: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.answer-btn.selected {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.answer-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.success-message {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}

.error-message {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}
</style>