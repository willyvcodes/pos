<script>
    import TabContent from "../pages/components/TabContent.svelte";

    import { user, logout } from "../helpers/stores";

    let isSidebarHidden = true;
    let isNavbarToggled = false;

    const toggleSidebar = () => {
        isSidebarHidden = !isSidebarHidden;
    };

    const toggleNabbar = () => {
        isNavbarToggled = !isNavbarToggled;
    };
</script>

<div class="container-fluid d-md-flex p-0 h-md-100">
    <div
        class="bg-nav {isSidebarHidden
            ? 'sidebar-hidden'
            : 'sidebar'} d-md-flex flex-column"
    >
        <!-- Logo -->
        <div class="sidebar-header p-3 text-center">
            <div class="logo-container">
                <i class="fas fa-store text-primary"></i>
                {#if !isSidebarHidden}
                    <span class="ms-2 fw-bold">Shop POS</span>
                {/if}
            </div>
        </div>

        <!-- nav -->
        <nav class="navbar navbar-dark flex-grow-1">
            <div class="container-fluid justify-content-md-center p-md-0">
                <button
                    class="navbar-toggler d-md-none"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                    on:click={toggleNabbar}
                >
                    {#if isNavbarToggled}
                        <i class="fas fa-bars"></i>
                    {:else}
                        <i class="fas fa-times"></i>
                    {/if}
                </button>
                <div
                    class="collapse navbar-collapse d-md-flex justify-content-center"
                    id="navbarNav"
                >
                    <ul class="navbar-nav nav">
                        <li class="nav-item">
                            <a
                                class="nav-link active"
                                data-bs-toggle="tab"
                                href="#orders"
                            >
                                <div class="nav-icon">
                                    <i class="fas fa-shopping-cart"></i>
                                </div>
                                {#if !isSidebarHidden}
                                    <span>Point of Sale</span>
                                {/if}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                data-bs-toggle="tab"
                                href="#management"
                            >
                                <div class="nav-icon">
                                    <i class="fas fa-box"></i>
                                </div>
                                {#if !isSidebarHidden}
                                    <span>Inventory</span>
                                {/if}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                data-bs-toggle="tab"
                                href="#profile"
                            >
                                <div class="nav-icon">
                                    <i class="fas fa-user-cog"></i>
                                </div>
                                {#if !isSidebarHidden}
                                    <span>Settings</span>
                                {/if}
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- User -->
        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar">
                    <span
                        >{$user.firstname
                            .substring(0, 1)
                            .toUpperCase()}{$user.lastname
                            .substring(0, 1)
                            .toUpperCase()}</span
                    >
                </div>
                {#if !isSidebarHidden}
                    <div class="user-details">
                        <span class="user-name">{$user.username}</span>
                        <span class="user-role"
                            >{$user.is_admin ? "Administrator" : "Staff"}</span
                        >
                    </div>
                {/if}
            </div>
            <div class="sidebar-actions">
                <button class="btn btn-link text-light" on:click={logout}>
                    <i class="fas fa-sign-out-alt"></i>
                    {#if !isSidebarHidden}
                        <span class="ms-2">Logout</span>
                    {/if}
                </button>
                <button
                    class="btn btn-link text-light d-none d-md-block"
                    on:click={toggleSidebar}
                >
                    <i
                        class="fas {isSidebarHidden
                            ? 'fa-chevron-right'
                            : 'fa-chevron-left'}"
                    ></i>
                </button>
            </div>
        </div>
    </div>
    <div class="container-fluid p-0 bg-content">
        <TabContent />
    </div>
</div>

<style>
    @media (min-width: 768px) {
        .h-md-100 {
            height: 100%;
        }

        .sidebar-hidden {
            min-width: 64px !important;
        }

        .sidebar-hidden .navbar-nav .nav-item .nav-link span,
        .sidebar-hidden .user-details,
        .sidebar-hidden .sidebar-actions span {
            display: none;
        }
    }

    .bg-nav {
        background-color: #1a1f36;
        color: #fff;
    }

    .bg-content {
        background-color: #f8f9fa;
    }

    .sidebar {
        min-width: 240px;
        transition: all 0.3s ease;
    }

    .sidebar-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }

    .nav-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        margin-right: 12px;
        transition: all 0.3s ease;
    }

    .nav-link {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        color: rgba(255, 255, 255, 0.7) !important;
        transition: all 0.3s ease;
    }

    .nav-link:hover {
        color: #fff !important;
        background: rgba(255, 255, 255, 0.1);
    }

    .nav-link.active {
        color: #fff !important;
        background: rgba(255, 255, 255, 0.1);
    }

    .nav-link.active .nav-icon {
        background: rgba(255, 255, 255, 0.1);
    }

    .sidebar-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
    }

    .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }

    .user-avatar {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
    }

    .user-details {
        margin-left: 12px;
    }

    .user-name {
        display: block;
        font-weight: 600;
    }

    .user-role {
        display: block;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
    }

    .sidebar-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .sidebar-actions .btn-link {
        text-decoration: none;
        padding: 8px;
        border-radius: 4px;
    }

    .sidebar-actions .btn-link:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .navbar-toggler {
        border: none;
        padding: 0.5rem;
    }

    .navbar-toggler:focus {
        box-shadow: none;
    }
</style>
