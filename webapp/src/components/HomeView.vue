<template>
    <div class="home">
      <h1>Welcome to Percept</h1>
      <div class="button-container">
        <button @click="$emit('participate')" class="btn">Participate</button>
        <button @click="$emit('create')" class="btn">Create</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomeView'
  }
  </script>
  
  <style scoped>
  .button-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
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