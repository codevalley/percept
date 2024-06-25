<template>
    <div class="participate">
      <h2>Enter Survey Code</h2>
      <form @submit.prevent="submitCode">
        <input v-model="code" type="text" placeholder="Survey Code" required>
        <button type="submit" class="btn">Enter</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ParticipateView',
    data() {
      return {
        code: ''
      }
    },
    methods: {
      submitCode() {
        this.$emit('submit-code', this.code);
      }
    }
  }
  </script>
  
  <style scoped>
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }
  
  input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 200px;
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
  
  .btn:hover {
    background-color: #2980b9;
  }
  </style>