"""Tools for the resolutions agent."""

# ruff: noqa: E501

import json
import os
import random
import uuid
from datetime import datetime, timedelta

from vertexai import rag
from vertexai.generative_models import GenerativeModel

from utils import extract_and_concatenate_rag_content  # type: ignore

summary_model = GenerativeModel(
    model_name=os.environ.get('GOOGLE_CLOUD_LLM_NAME', '')
)


def get_instructions_for_user_motivation(
    intent: str, customer_motivation: str
) -> str:
    """Classifies the user intent based on the provided information.

    Args:
        intent (str): A high level generic title for the user's intent.
        customer_motivation (str): A brief description of the user's motivation
            for contacting The Home Depot.

    Returns:
        str: If an intent is identified then the function will return
        step-by-step instructions to resolve the user's intent. Otherwise,
        it will return a message asking the user for more clarity on
        their intent.

    Example:
        >>> get_instructions_for_user_motivation(
                 intent = "Account Security",
                 customer_motivation = "The customer is experiencing issues
                    with their Home Depot account, such as orders not
                    appearing, unauthorized access attempts, or
                    difficulty linking purchases to their account."
    """
    print('\n\n\n\n\nClassifying intent...........')
    response = (
        'I am struggling to understand. Please provide more details '
        'about your reason for contacting The Home Depot so I can assist you '
        'better.'
    )

    if intent:
        text = f"""Intent: {intent},
        Customer Motivation: {customer_motivation}"""

        # Direct context retrieval
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=3,
        )

        try:
            response = rag.retrieval_query(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=os.environ.get('RAG_CORPUS'),
                    )
                ],
                text=text,
                rag_retrieval_config=rag_retrieval_config,
            )

            response = extract_and_concatenate_rag_content(response)

            prompt = f"""Given the following intent and customer motivation,
            {text}
            and the following step-by-step instructions retrieved from the
            RAG engine,
            {response}
            Please summarize the likely step-by-step instructions an agent
            would need to follow to resolve the given intent and customer
            motivation.
            """

            response = summary_model.generate_content(prompt)
            response = response.text.strip()

        except Exception as e:
            print(f'Error during RAG retrieval: {e}')

    print(f'RESPONSE: {response}')
    print('Returning response...\n\n\n\n\n\n\n\n\n')
    return response  # type: ignore


ORDER_CACHE = {}

PRODUCTS = {
    'DRILL': {
        'name': 'DeWalt 20V MAX Cordless Drill/Driver Kit',
        'price': '$149.99',
        'sku': 'DCD778C2',
        'category': 'Power Tools',
    },
    'DOOR': {
        'name': '36 in. x 80 in. Craftsman 6-Lite Prefinished Mahogany Front Door',
        'price': '$499.99',
        'sku': 'HDPFD6MH36',
        'category': 'Doors & Windows',
    },
    'PLANT': {
        'name': '10 in. Monstera Deliciosa Indoor Plant in Decorative Planter',
        'price': '$49.99',
        'sku': 'MONSPLNT10',
        'category': 'Garden Center',
    },
    'SAW': {
        'name': 'RYOBI 10 in. 15 Amp Table Saw',
        'price': '$299.99',
        'sku': 'RTS12',
        'category': 'Power Tools',
    },
    'LIGHT': {
        'name': 'Hampton Bay 52 in. LED Indoor Brushed Nickel Ceiling Fan with Light',
        'price': '$129.99',
        'sku': 'CF52BN',
        'category': 'Lighting',
    },
}

# Create a persistent store for order details
ORDER_CACHE = {}

# ==== TOOLS ====


def check_order_status(order_id: str) -> str:
    """Check the current status of an order including remorse period information.

    Args:
        order_id: The order ID to check

    Returns:
        Order status information in JSON format
    """
    print(f'TOOL USED: check_order_status for {order_id}')
    now = datetime.now()

    if order_id not in ORDER_CACHE:
        # First time seeing this order ID, generate and store data
        # Select a random product
        product_key = random.choice(list(PRODUCTS.keys()))
        product = PRODUCTS[product_key]

        # Status based on order prefix
        if order_id.startswith('WN'):
            # Processing randomization
            minutes_ago = random.randint(0, 45)
            order_timestamp = now - timedelta(minutes=minutes_ago)
            status = 'PROCESSING'
            delivery_date = now + timedelta(days=5)
            payment_method = 'Credit Card'
            amount = product['price']
        elif order_id.startswith('WG'):
            # Shipped orders from 1-3 days ago
            days_ago = random.randint(1, 3)
            order_timestamp = now - timedelta(days=days_ago)
            status = 'SHIPPED'
            delivery_date = now + timedelta(days=2)
            payment_method = 'Debit Card'
            amount = product['price']
        else:
            # Delivered orders from 4-10 days ago
            days_ago = random.randint(4, 10)
            order_timestamp = now - timedelta(days=days_ago)
            status = 'DELIVERED'
            delivery_date = now - timedelta(days=1)
            payment_method = 'PayPal'
            amount = product['price']

        # Store data in cache
        ORDER_CACHE[order_id] = {
            'order_timestamp': order_timestamp,
            'status': status,
            'delivery_date': delivery_date,
            'payment_method': payment_method,
            'amount': amount,
            'product': product,
        }

    # Use cached data for consistency
    cached_order = ORDER_CACHE[order_id]
    order_timestamp = cached_order['order_timestamp']

    # Calculate remorse using cache
    remorse_end_time = order_timestamp + timedelta(minutes=45)
    in_remorse_period = now < remorse_end_time
    remorse_minutes_left = max(
        0, int((remorse_end_time - now).total_seconds() / 60)
    )

    response = {
        'order_id': order_id,
        'order_timestamp': order_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'status': cached_order['status'],
        'payment_method': cached_order['payment_method'],
        'total_amount': cached_order['amount'],
        'product': cached_order['product'],
        'estimated_delivery': cached_order['delivery_date'].strftime(
            '%Y-%m-%d'
        )
        if cached_order['status'] != 'DELIVERED'
        else None,
        'delivery_date': cached_order['delivery_date'].strftime('%Y-%m-%d')
        if cached_order['status'] == 'DELIVERED'
        else None,
        'remorse_period': {
            'in_remorse_period': in_remorse_period,
            'minutes_left': remorse_minutes_left,
            'can_self_cancel': in_remorse_period,
        },
        'can_cancel': in_remorse_period,
        'can_return': cached_order['status'] in ['SHIPPED', 'DELIVERED'],
    }

    return json.dumps(response, indent=2)


def cancel_order(order_id: str) -> str:
    """Cancel an order if it's still in processing status.

    Args:
        order_id: The order ID to cancel

    Returns:
        Cancellation status in JSON format
    """
    print(f'TOOL USED: cancel_order for {order_id}')

    # First check order status
    status_info = json.loads(check_order_status(order_id))

    # Determine if order can be cancelled based on status and remorse period
    success = status_info['can_cancel']
    easy_cancel = status_info.get('remorse_period', {}).get(
        'in_remorse_period', False
    )

    if success:
        cancellation_id = f'CAN-{uuid.uuid4().hex[:8].upper()}'
        refund_id = f'REF-{uuid.uuid4().hex[:8].upper()}'
        refund_status = 'PROCESSING'
        refund_amount = status_info['total_amount']
        estimated_refund_date = (datetime.now() + timedelta(days=3)).strftime(
            '%Y-%m-%d'
        )
        payment_method = status_info['payment_method']

        if easy_cancel:
            message = f"Your order for {status_info['product']['name']} has been instantly cancelled as it's within the 45-minute remorse period. Your refund of {refund_amount} is being processed."
            refund_speed = '1-2 business days'
        else:
            message = f'Your order for {status_info["product"]["name"]} has been cancelled. Your refund of {refund_amount} is being processed.'
            refund_speed = '3-5 business days'

        # Update cache to reflect cancelled status
        if order_id in ORDER_CACHE:
            ORDER_CACHE[order_id]['status'] = 'CANCELLED'
    else:
        cancellation_id = None
        refund_id = None
        refund_status = None
        refund_amount = None
        estimated_refund_date = None
        payment_method = None
        refund_speed = None
        message = f'Unable to cancel this order for {status_info["product"]["name"]} - it may already be shipped or delivered, or outside the remorse period'

    response = {
        'success': success,
        'order_id': order_id,
        'product': status_info['product'],
        'status': 'CANCELLED' if success else 'CANCELLATION_FAILED',
        'cancellation_id': cancellation_id,
        'refund_id': refund_id,
        'refund_status': refund_status,
        'refund_amount': refund_amount,
        'payment_method': payment_method,
        'estimated_refund_date': estimated_refund_date,
        'refund_speed': refund_speed,
        'in_remorse_period': easy_cancel,
        'message': message,
    }

    return json.dumps(response, indent=2)


def initiate_return(
    order_id: str, reason: str, return_method: str = 'ship'
) -> str:
    """Initiate a return for a shipped or delivered order with flexible return options.

    Args:
        order_id: The order ID
        reason: Reason for the return (e.g., "damaged", "not needed")
        return_method: How the customer wants to return the item:
                     "ship" - Get a return shipping label to print at home
                     "store" - Return at a nearby Home Depot store
                     "postal" - Drop off at a nearby postal office

    Returns:
        Return request information in JSON format
    """
    print(
        f'TOOL USED: initiate_return for order {order_id}, reason: {reason}, method: {return_method}'
    )

    # Validate return method
    valid_methods = ['ship', 'store', 'postal']
    if return_method not in valid_methods:
        return json.dumps(
            {
                'success': False,
                'message': f'Invalid return method. Please choose from: {", ".join(valid_methods)}',
                'status': 'INVALID_RETURN_METHOD',
            },
            indent=2,
        )

    # First check the order status
    status_info = json.loads(check_order_status(order_id))

    # Check if order can be returned (WG or other orders, not WN or must be outside remorse period)
    success = status_info['status'] in ['SHIPPED', 'DELIVERED']

    if success:
        return_id = f'RET-{uuid.uuid4().hex[:8].upper()}'
        refund_id = f'REF-{uuid.uuid4().hex[:8].upper()}'

        product_name = status_info['product']['name']
        refund_amount = status_info['total_amount']

        # Handle different return methods
        if return_method == 'ship':
            return_location = 'using the prepaid shipping label'
            instructions = f"We'll email you a prepaid return shipping label to print at home. Package the {product_name} securely and attach the label."
        elif return_method == 'store':
            return_location = 'at a nearby Home Depot store'
            instructions = f'You can return the {product_name} to any Home Depot store. Bring your order receipt or ID. The nearest stores can be found on our website or app.'
        else:  # postal
            return_location = 'at a nearby postal office'
            instructions = f"We'll email you a prepaid return label. Take the packaged {product_name} with the attached label to any USPS, UPS, or FedEx location."

        # Fix the logical inconsistency with SHIPPED items
        if status_info['status'] == 'SHIPPED':
            # Only use this logic if the item isn't reported as damaged/broken
            status = 'RETURN_INITIATED_FOR_SHIPPED_ITEM'
            next_steps = f'Please keep the {product_name} when it arrives and return it {return_location}. {instructions}'
        else:
            # For DELIVERED items or if the customer reports damage/breakage
            status = 'RETURN_INITIATED_FOR_DELIVERED_ITEM'
            next_steps = f'Please return the {product_name} {return_location}. {instructions}'

        message = (
            f'Return initiated successfully for {product_name}. {next_steps}'
        )

        # Update cache to reflect return status
        if order_id in ORDER_CACHE:
            ORDER_CACHE[order_id]['status'] = 'RETURN_INITIATED'
            ORDER_CACHE[order_id]['return_method'] = return_method
    else:
        return_id = None
        refund_id = None
        status = 'RETURN_FAILED'
        return_location = None
        instructions = None
        refund_amount = None
        message = f'Unable to process return for {status_info["product"]["name"]} - the order is still being processed. Please try cancelling instead.'

    response = {
        'success': success,
        'order_id': order_id,
        'product': status_info['product'],
        'return_id': return_id,
        'refund_id': refund_id if success else None,
        'status': status,
        'reason': reason,
        'return_method': return_method if success else None,
        'return_instructions': instructions if success else None,
        'refund_amount': refund_amount,
        'estimated_refund_date': (datetime.now() + timedelta(days=7)).strftime(
            '%Y-%m-%d'
        )
        if success
        else None,
        'message': message,
    }

    return json.dumps(response, indent=2)
