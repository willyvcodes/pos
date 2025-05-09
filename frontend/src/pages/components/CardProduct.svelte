<script>
    export let product = "";
    export let callback = () => {};
</script>

<div class="col-lg-3 col-md-4 col-6 mb-3" on:click={() => callback()}>
    <div class="card h-100 border-0 position-relative product-card">
        <div class="product-image-container">
            <img
                src={product.thumbnail}
                class="product-img"
                alt={product.name}
            />
            <div class="mask-top-left">
                <span class="badge bg-success fs-6"
                    >${product.price.toFixed(2)}</span
                >
            </div>
        </div>
        <div class="card-body p-3 text-center">
            <h5 class="product-name mb-1">{product.name}</h5>
            <p class="product-type text-muted mb-0">{product.type}</p>
        </div>
        <div class="quick-add">
            <button
                class="btn btn-primary btn-sm"
                on:click|stopPropagation={() => callback()}
            >
                <i class="fas fa-plus"></i> Add
            </button>
        </div>
    </div>
</div>

<style>
    .product-card {
        transition: all 0.3s ease;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .product-card:active {
        transform: scale(0.98);
    }

    .product-image-container {
        position: relative;
        padding-top: 100%;
        overflow: hidden;
    }

    .product-img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .product-card:hover .product-img {
        transform: scale(1.05);
    }

    .mask-top-left {
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 2;
    }

    .product-name {
        font-size: 1.1rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .product-type {
        font-size: 0.9rem;
    }

    .quick-add {
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 2;
        background: rgba(255, 255, 255, 0.9);
        padding: 4px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
    }

    .product-card:hover .quick-add {
        opacity: 1;
        bottom: 15px;
    }

    .quick-add .btn {
        min-width: 80px;
        font-weight: 500;
    }

    @media (max-width: 768px) {
        .quick-add {
            opacity: 1;
            bottom: 5px;
            background: rgba(255, 255, 255, 0.95);
        }

        .product-card {
            margin-bottom: 1rem;
        }

        .product-name {
            font-size: 1rem;
        }

        .product-type {
            font-size: 0.8rem;
        }
    }
</style>
