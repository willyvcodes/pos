<script>
    import { show_toaster, show_confirm_dialog } from "../helpers/alerts";

    import { login_user, create_user } from "../helpers/http_requests";
    import { user } from "../helpers/stores";

    let username,
        password = "";
    let showRegister = false;
    let reg_username = "",
        reg_password = "",
        reg_email = "";

    const handle_login = async () => {
        try {
            const resp = await login_user({
                username: username,
                password: password,
            });

            if (resp.ok) {
                const data = await resp.json();
                // Store tokens in localStorage
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                // Get user data
                const userResp = await fetch("/api/users/me", {
                    headers: {
                        Authorization: `Bearer ${data.access_token}`,
                    },
                });

                if (userResp.ok) {
                    $user = await userResp.json();
                    show_toaster("success", `Welcome ${username}`);
                }
            } else {
                const error = await resp.json();
                show_toaster("error", error.detail || "Login failed");
            }
        } catch (error) {
            show_toaster("error", "An error occurred during login");
        }
    };

    const handle_keypress = (e) => {
        if (e.key == "Enter") {
            handle_login();
        }
    };

    const handle_register = async () => {
        try {
            const resp = await create_user({
                username: reg_username,
                password: reg_password,
                email: reg_email,
                firstname: reg_username, // Using username as firstname for simplicity
                lastname: "", // Empty lastname for simplicity
                phone: "", // Empty phone for simplicity
            });

            if (resp.ok) {
                show_toaster("success", `Account created for ${reg_username}`);
                showRegister = false;
            } else {
                const error = await resp.json();
                show_toaster(
                    "error",
                    error.detail || "Could not create account",
                );
            }
        } catch (error) {
            show_toaster("error", "An error occurred during registration");
        }
    };
</script>

<div class="container h-100">
    <div class="row h-100 d-flex justify-content-center align-items-center">
        <div class="col-12 col-md-4">
            <div class="form-group bg-light p-4 rounded shadow-md">
                <div class="text-center mb-4">
                    <i class="fas fa-store text-primary fs-1"></i>
                    <h4 class="mt-2"><b>Shop POS</b></h4>
                </div>
                <label for="user_login" class="form-label">Username</label>
                <input
                    type="text"
                    class="form-control mb-3"
                    id="user_login"
                    placeholder="Enter your username"
                    bind:value={username}
                    on:keypress={handle_keypress}
                />
                <label for="user_password" class="form-label">Password</label>
                <input
                    type="password"
                    class="form-control mb-4"
                    id="user_password"
                    placeholder="Enter your password"
                    bind:value={password}
                    on:keypress={handle_keypress}
                />
                <button
                    class="btn btn-primary btn-lg w-100 mb-3"
                    on:click={handle_login}
                >
                    Sign In
                </button>
                <button
                    class="btn btn-link w-100 text-secondary"
                    on:click={() => (showRegister = true)}
                >
                    Create Account
                </button>
            </div>
        </div>
    </div>
    {#if showRegister}
        <div
            class="modal d-block"
            tabindex="-1"
            style="background: var(--overlay-dark);"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Create Account</h5>
                        <button
                            type="button"
                            class="btn-close"
                            on:click={() => (showRegister = false)}
                        ></button>
                    </div>
                    <div class="modal-body">
                        <label for="reg_username" class="form-label"
                            >Username</label
                        >
                        <input
                            id="reg_username"
                            class="form-control mb-3"
                            placeholder="Choose a username"
                            bind:value={reg_username}
                        />
                        <label for="reg_email" class="form-label">Email</label>
                        <input
                            id="reg_email"
                            class="form-control mb-3"
                            type="email"
                            placeholder="Enter your email"
                            bind:value={reg_email}
                        />
                        <label for="reg_password" class="form-label"
                            >Password</label
                        >
                        <input
                            id="reg_password"
                            class="form-control mb-3"
                            type="password"
                            placeholder="Choose a password"
                            bind:value={reg_password}
                        />
                    </div>
                    <div class="modal-footer">
                        <button
                            class="btn btn-outline-secondary"
                            on:click={() => (showRegister = false)}
                        >
                            Cancel
                        </button>
                        <button
                            class="btn btn-primary"
                            on:click={handle_register}
                        >
                            Create Account
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .shadow-md {
        box-shadow: var(--shadow-md) !important;
    }

    .form-label {
        color: var(--text-secondary);
        font-weight: 500;
    }

    .modal-content {
        border: none;
    }

    .btn-close {
        color: var(--text-secondary);
    }

    .btn-link {
        text-decoration: none;
    }

    .btn-link:hover {
        text-decoration: underline;
    }
</style>
