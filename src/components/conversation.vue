<template>
  <div>
    <message
      v-for="message in messages"
      :key="message.id"
      v-bind:message="message"></message>
  </div>
</template>

<script>
  import message from './message.vue'

  export default {
    name: 'conversation',
    data: function() {
      return {
        messages: []
      }
    },
    methods: {
      async getMessages() {
        let res = await fetch('/api/messages', { credentials: 'same-origin'})
        this.messages = await res.json()
      }
    },
    created() {
      this.getMessages()
    },
    components: {
      message
    }
  }
</script>

<styles>

</styles>
