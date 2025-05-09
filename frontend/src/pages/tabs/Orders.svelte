<script>
    import { Input } from "sveltestrap";
    import { show_toaster, show_confirm_dialog } from "../../helpers/alerts";
    import CardProduct from "../components/CardProduct.svelte";
    import ModalAddToCart from "../modals/ModalAddToCart.svelte";
    import ModalOrderHistory from "../modals/ModalOrderHistory.svelte";

    // http requests
    import {
        get_all_products,
        create_checkout_session,
        create_new_order,
        update_order_by_id,
    } from "../../helpers/http_requests";

    let products = [];
    let cartItems = [];
    let order_id = "";

    let visible_products = [];
    let search = "";
    let total;

    // Modal
    let modal_add_to_cart;
    let modal_order_history;

    let selected_item;

    // DATE
    const date = new Date();
    let currentDate = date.toDateString().slice(0, -4);

    let old_order = "";
    let open_order = false;

    // stripe
    const new_checkout_session = async () => {
        let checkout_items = [];
        cartItems.forEach((item) => {
            checkout_items.push({
                name: item.name,
                quantity: item.amount,
                price: parseInt(item.price * 100),
                thumbnail: item.thumbnail,
            });
        });

        save_order();

        const resp = await create_checkout_session(checkout_items);
        if (resp.ok) {
            const data = await resp.json();
            if (data.url) {
                window.location.href = data.url;
            } else {
                show_toaster("error", "Could not create checkout session");
            }
        } else {
            show_toaster("error", "Could not create checkout session");
        }
    };
    //

    $: visible_products = search
        ? products.filter((product) => {
              let product_name = product.name.toLowerCase();
              let product_type = product.type.toLowerCase();
              if (
                  product_name.includes(search.toLowerCase()) ||
                  product_type.includes(search.toLowerCase()) ||
                  product.upc.includes(search)
              )
                  return product;
          })
        : products;

    $: total = cartItems.reduce((p, c) => {
        return p + c.price * c.amount;
    }, 0);

    $: if (old_order) {
        cartItems = old_order.products;
        order_id = old_order._id;
        open_order = true;
    }

    const pull_all_products = async () => {
        const resp = await get_all_products();
        if (resp.ok) {
            products = await resp.json();
        }
    };

    const handle_add_to_cart = (new_item) => {
        const index = cartItems.findIndex(
            (existing_item) => existing_item._id === new_item._id,
        );
        if (index == -1) {
            new_item.amount = 1;
        } else {
            new_item.amount = cartItems[index].amount;
        }
        selected_item = new_item;
        modal_add_to_cart.open_add_to_cart();
    };

    const delete_item_from_cart = (item) => {
        const index = cartItems.findIndex(
            (existing_item) => existing_item._id === item._id,
        );
        show_confirm_dialog(
            "Remove Product",
            `Are you sure you want to remove "${item.name}?"`,
            "Remove",
            "Cancel",
            async () => {
                if (index == -1) {
                    show_toaster("error", "Item Could Not Be Removed!");
                } else {
                    cartItems.splice(index, 1);
                    cartItems = cartItems;
                    show_toaster(
                        "success",
                        `${item.name} Successfully Removed`,
                    );
                }
            },
        );
    };

    const save_order = async () => {
        const order = {
            products: cartItems,
            total: total.toFixed(2),
        };

        let resp;
        if (order_id) {
            resp = await update_order_by_id(order, order_id);
        } else {
            resp = await create_new_order(order);
        }

        if (!resp.ok) {
            console.log("Could Not Save Order");
        }
    };

    const handle_open_order = () => {
        open_order = !open_order;
        if (!open_order) {
            cartItems = [];
            old_order = "";
            order_id = "";
        }
    };

    const handle_cancel_order = () => {
        show_confirm_dialog(
            "Cancel Order",
            `Are you sure want to cancel this order?`,
            "Cancel Order",
            "Continue",
            async () => {
                cartItems = [];
                old_order = "";
                order_id = "";
                handle_open_order();
            },
        );
    };

    const handle_order_history = () => {
        modal_order_history.open_order_history();
    };

    const update_quantity = (item, change) => {
        const index = cartItems.findIndex(
            (existing_item) => existing_item._id === item._id,
        );
        if (index !== -1) {
            const newAmount = cartItems[index].amount + change;
            if (newAmount > 0) {
                cartItems[index].amount = newAmount;
                cartItems = cartItems; // Trigger reactivity
            } else if (newAmount === 0) {
                delete_item_from_cart(item);
            }
        }
    };
</script>

<div class="tab-pane fade show active h-100" id="orders" role="tab">
    <div class="container-fluid h-100">
        {#if open_order}
            <div class="row h-100">
                <div class="col-12 col-md-8 col-xl-9">
                    <!-- products heading -->
                    <div class="container-fluid my-2 py-3 bg-light rounded">
                        <div class="row align-items-center">
                            <div class="col-md-8 col-7">
                                <div class="input-group">
                                    <span
                                        class="input-group-text bg-white border-end-0"
                                    >
                                        <i class="fas fa-search text-muted"></i>
                                    </span>
                                    <Input
                                        type="search"
                                        bind:value={search}
                                        placeholder="Search For Item Name, Type, UPC..."
                                        class="border-start-0"
                                    />
                                </div>
                            </div>
                            <div
                                class="col-md-4 col-5 d-flex justify-content-end gap-2"
                            >
                                <button
                                    class="btn btn-outline-primary"
                                    on:click={() => handle_order_history()}
                                >
                                    <i class="fas fa-history"></i>
                                    <span class="d-none d-md-inline ms-1"
                                        >History</span
                                    >
                                </button>
                                <button
                                    class="btn btn-warning"
                                    on:click={() => handle_cancel_order()}
                                >
                                    <i class="fas fa-times"></i>
                                    <span class="d-none d-md-inline ms-1"
                                        >Cancel</span
                                    >
                                </button>
                            </div>
                        </div>
                    </div>
                    <!-- products -->
                    <div class="menu-container">
                        <div class="row g-3">
                            {#await pull_all_products()}
                                <div class="col-12 text-center py-5">
                                    <div
                                        class="spinner-border text-primary"
                                        role="status"
                                    >
                                        <span class="visually-hidden"
                                            >Loading...</span
                                        >
                                    </div>
                                </div>
                            {:then}
                                {#each visible_products as item}
                                    <CardProduct
                                        product={item}
                                        callback={() =>
                                            handle_add_to_cart(item)}
                                    />
                                {/each}
                            {:catch error}
                                <div class="col-12 text-center py-5">
                                    <div
                                        class="alert alert-danger"
                                        role="alert"
                                    >
                                        <i
                                            class="fas fa-exclamation-circle me-2"
                                        ></i>
                                        Could Not Load Products
                                    </div>
                                </div>
                            {/await}
                        </div>
                    </div>
                </div>
                <div
                    class="col-12 col-md-4 col-xl-3 px-1 py-3 min-vh-100 checkout-container"
                    id="checkout_section"
                >
                    <div class="container-fluid d-flex flex-column h-100">
                        <div class="checkout-heading">
                            <div class="row">
                                <div class="col-6">
                                    <span
                                        class="fas fa-shopping-cart fs-3 text-success"
                                    ></span>
                                </div>
                                <div class="col-6 text-end">
                                    <h5>{currentDate}</h5>
                                </div>
                            </div>
                            <hr />
                        </div>
                        <div class="checkout-items">
                            {#each cartItems as item}
                                <div class="checkout-item">
                                    <div
                                        class="d-flex justify-content-between align-items-center"
                                    >
                                        <div class="d-flex align-items-center">
                                            <img
                                                src={item.thumbnail}
                                                alt={item.name}
                                                class="checkout-item-img"
                                            />
                                            <div class="ms-2">
                                                <h6 class="mb-0">
                                                    {item.name}
                                                </h6>
                                                <small class="text-muted"
                                                    >${item.price.toFixed(2)} each</small
                                                >
                                            </div>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <div class="quantity-controls me-2">
                                                <button
                                                    class="btn btn-sm btn-outline-secondary"
                                                    on:click={() =>
                                                        update_quantity(
                                                            item,
                                                            -1,
                                                        )}
                                                >
                                                    <i class="fas fa-minus"></i>
                                                </button>
                                                <span class="mx-2"
                                                    >{item.amount}</span
                                                >
                                                <button
                                                    class="btn btn-sm btn-outline-secondary"
                                                    on:click={() =>
                                                        update_quantity(
                                                            item,
                                                            1,
                                                        )}
                                                >
                                                    <i class="fas fa-plus"></i>
                                                </button>
                                            </div>
                                            <button
                                                class="btn btn-sm btn-outline-danger"
                                                on:click={() =>
                                                    delete_item_from_cart(item)}
                                            >
                                                <i class="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                        <div class="checkout-pay">
                            <hr />
                            <div class="row">
                                <div class="col-12">
                                    <div
                                        class="d-flex justify-content-between align-items-center mb-3"
                                    >
                                        <h5 class="mb-0">Total:</h5>
                                        <h4 class="mb-0 text-success">
                                            ${total.toFixed(2)}
                                        </h4>
                                    </div>
                                    <button
                                        class="btn btn-success btn-pay fs-4 {cartItems.length ==
                                        0
                                            ? 'disabled'
                                            : ''}"
                                        on:click={() => new_checkout_session()}
                                    >
                                        <i class="fas fa-credit-card me-2"></i>
                                        Pay Now
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {:else}
            <div class="order-container">
                <button
                    class="btn btn-success btn-lg"
                    on:click={handle_open_order}
                >
                    <h2 class="m-0 p-3">New Order</h2>
                </button>
                <button
                    class="btn btn-primary btn-md"
                    on:click={handle_order_history}
                >
                    <i class="fas fa-history me-2"></i>
                    <span class="m-0">History</span>
                </button>
            </div>
        {/if}
    </div>

    <!-- modals -->
    <ModalAddToCart
        bind:this={modal_add_to_cart}
        bind:item={selected_item}
        bind:itemList={cartItems}
    />
    <ModalOrderHistory
        bind:this={modal_order_history}
        bind:loaded_order={old_order}
    />
</div>

<style>
    @media (min-width: 768px) {
        .checkout-container {
            border-radius: 18px 0px 0px 18px !important;
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
        }
    }

    .order-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        padding-top: 20px;
    }

    .menu-container {
        height: calc(100vh - 80px);
        padding: 1rem;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .checkout-container {
        border-radius: 0;
        background-color: white;
    }

    .checkout-items {
        height: calc(100vh - 250px);
        padding: 1rem;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .checkout-item {
        padding: 0.75rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        margin-bottom: 0.5rem;
    }

    .checkout-item-img {
        width: 50px;
        height: 50px;
        object-fit: cover;
        border-radius: 4px;
    }

    .quantity-controls {
        display: flex;
        align-items: center;
        background-color: white;
        border-radius: 4px;
        padding: 2px;
    }

    .checkout-pay {
        margin-top: auto;
        padding: 1rem;
        background-color: white;
    }

    .btn-pay {
        height: 56px;
        width: 100%;
        border-radius: 8px;
    }

    :global(.input-group-text) {
        border-right: none;
    }

    :global(.input-group .form-control) {
        border-left: none;
    }

    :global(.input-group .form-control:focus) {
        box-shadow: none;
        border-color: #ced4da;
    }
</style>
