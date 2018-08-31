<template>
    <div>
      <conversation></conversation>
      <a href="/login" v-if="!username">Login</a>
      <button v-on:click="logout" v-if="username">Logout</button>
      <div>USERNAME: {{username}}</div>
    </div>
</template>

<script>
  import conversation from './components/conversation.vue'

  export default {
    name: 'app',
    components: {
      conversation
    },
    methods: {
      async login() {
        await fetch('/api/login', {
          body: JSON.stringify({username: 'anna'}),
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json"
          },
          method: 'POST'
        })
        this.username = 'anna'
      },

      async logout() {
        await fetch('/api/logout', {
          method: 'POST',
          credentials: "same-origin"
        })
        this.username = null
      }
    },
    data: function() {
      return {
        username: null
      }
    }
  }
</script>

<styles>

</styles>
