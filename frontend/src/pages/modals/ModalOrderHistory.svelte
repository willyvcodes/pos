<script>
    import {
        Button,
        Modal,
        ModalBody,
        ModalFooter,
        ModalHeader,
    } from "sveltestrap";
    import {
        get_all_orders,
        clear_all_orders,
    } from "../../helpers/http_requests";
    import { show_toaster, show_confirm_dialog } from "../../helpers/alerts";

    // props
    export let loaded_order = "";
    let orders = [];

    // modal config
    let order_history_open = false;
    let size = "lg";

    let selected_row = 0;

    export const open_order_history = () => {
        order_history_open = !order_history_open;
        selected_row = 0;
    };

    const pull_all_orders = async () => {
        const resp = await get_all_orders();
        if (resp.ok) {
            orders = await resp.json();
        }
    };

    const handle_table_selection = (index) => {
        selected_row = index;
    };

    const load_order = () => {
        loaded_order = orders[selected_row - 1];
        open_order_history();
    };

    const clear_history = async () => {
        show_confirm_dialog(
            "Clear Order History",
            "Are you sure you want to clear all order history? This action cannot be undone.",
            "Yes, Clear All",
            "Cancel",
            async () => {
                const resp = await clear_all_orders();
                if (resp.ok) {
                    const result = await resp.json();
                    show_toaster("success", result.detail);
                    orders = [];
                    selected_row = 0;
                } else {
                    const error = await resp.json();
                    show_toaster(
                        "error",
                        error.detail || "Failed to clear order history",
                    );
                }
            },
        );
    };
</script>

<Modal isOpen={order_history_open} {open_order_history} {size} scrollable>
    <ModalHeader {open_order_history}>Order History</ModalHeader>
    <ModalBody>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0">Total Orders: {orders.length}</h5>
            <Button color="danger" on:click={clear_history}>
                <i class="fas fa-trash-alt me-2"></i>Clear History
            </Button>
        </div>
        <table class="table table-hover table-responsive">
            <thead class="table-dark">
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Date Created</th>
                    <th scope="col">Products In Order</th>
                    <th scope="col">Total</th>
                </tr>
            </thead>
            <tbody>
                {#await pull_all_orders()}
                    <p>Loading Orders</p>
                {:then}
                    {#if orders.length === 0}
                        <tr>
                            <td colspan="4" class="text-center py-4">
                                <p class="text-muted mb-0">No orders found</p>
                            </td>
                        </tr>
                    {:else}
                        {#each orders as order, index}
                            <tr
                                class={selected_row == index + 1
                                    ? "table-primary"
                                    : ""}
                                on:click={() =>
                                    handle_table_selection(index + 1)}
                            >
                                <td><b>{index + 1}</b></td>
                                <td>{order.date_created.slice(0, 10).trim()}</td
                                >
                                <td>
                                    {#each order.products as product}
                                        <h6>
                                            {product.name} x{product.amount}
                                        </h6>
                                    {/each}
                                </td>
                                <td><b>${order.total}</b></td>
                            </tr>
                        {/each}
                    {/if}
                {:catch error}
                    <p>ERROR: Could Not Load Products {error}</p>
                {/await}
            </tbody>
        </table>
    </ModalBody>
    <ModalFooter>
        <Button color="danger" on:click={open_order_history}>Cancel</Button>
        <Button
            color="success"
            on:click={load_order}
            disabled={selected_row === 0}>Load Order</Button
        >
    </ModalFooter>
</Modal>

<style>
    :global(.table) {
        margin-bottom: 0;
    }

    :global(.table td) {
        vertical-align: middle;
    }

    :global(.table-hover tbody tr:hover) {
        cursor: pointer;
        background-color: var(--neutral-100);
    }

    :global(.table-primary) {
        background-color: var(--primary-light) !important;
    }
</style>
