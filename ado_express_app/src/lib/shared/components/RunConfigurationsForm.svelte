<script lang="ts">
  let name = "";
  let email = "";
  let message = "";

  function handleSubmit() {
    const formData = {
      name: name,
      email: email,
      message: message,
    };

    console.log(formData);
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div class="mb-4">
    <label for="name" class="block text-gray-700 font-bold mb-2">Name</label>
    <input
      type="text"
      id="name"
      class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      bind:value={name}
    />
  </div>

  <div class="mb-4">
    <label for="email" class="block text-gray-700 font-bold mb-2">Email</label>
    <input
      type="email"
      id="email"
      class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      bind:value={email}
    />
  </div>

  <div class="mb-4">
    <label for="message" class="block text-gray-700 font-bold mb-2"
      >Message</label
    >
    <textarea
      id="message"
      class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      rows="5"
      bind:value={message}
    />
  </div>

  <div class="flex justify-center">
    <button
      type="submit"
      class="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      Send Message
    </button>
  </div>
</form>