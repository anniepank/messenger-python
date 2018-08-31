<template>

  <div v-bind:style="{ backgroundColor: color }">
    <p class="underline"> {{message.content}} </p>
</div>

</template>

<script>

  export default {
    name: 'message',
    props: ['color', 'message'],
  }
</script>

<style lang="scss">
  .underline { text-decoration: underline; }
</style>
