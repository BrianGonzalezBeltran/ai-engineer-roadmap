with source as (
    select * from {{ source('stripe', 'payment') }}
),

renamed as (
    select
        id as payment_id,
        orderid as order_id,
        paymentmethod as payment_method,
        status,
        -- amount is in cents, convert to dollars
        amount / 100 as amount
        ,_batched_at
    from source
)

select * from renamed