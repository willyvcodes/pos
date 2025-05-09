<script>
  import Main from "./pages/Main.svelte";
  import Login from "./pages/Login.svelte";

  import { user } from "./helpers/stores";
  import "./styles/theme.css";
</script>

<main class="bg-dark">
  {#if !$user}
    <Login />
  {:else}
    <Main />
  {/if}
</main>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600&display=swap");

  :global(html, body, main) {
    font-family: var(--font-family) !important;
    font-weight: 400 !important;
    letter-spacing: 0.03rem;
    height: 100% !important;
    color: var(--text-primary);
    background-color: var(--bg-primary);
  }

  :global(.btn) {
    border-radius: var(--border-radius-md);
    transition: var(--transition-normal);
  }

  :global(.form-control) {
    border-radius: var(--border-radius-md);
    border-color: var(--border-color);
  }

  :global(.card) {
    border-radius: var(--border-radius-lg);
  }

  :global(.modal-content) {
    border-radius: var(--border-radius-lg);
  }
</style>
