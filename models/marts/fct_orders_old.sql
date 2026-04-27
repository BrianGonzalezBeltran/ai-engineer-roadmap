with orders as (
    select * from {{ ref('stg_jaffle_shop__orders') }}
),

payments as (
    select * from {{ ref('stg_stripe__payments') }}
),

final as (
    select
        orders.order_id,
        orders.customer_id,
        sum(payments.amount) as amount
    from orders
    left join payments on orders.order_id = payments.order_id
    where payments.status = 'success'
    group by orders.order_id, orders.customer_id
)

select * from final