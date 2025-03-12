import os
import asyncio
import random
from openai import OpenAI
from honeyhive import aevaluator
from honeyhive.async_api import evaluate as async_evaluate


# Create function to be evaluated
# inputs -> parameter to which datapoint or json value will be passed
# (optional) ground_truths -> ground truth value for the input
async def function_to_evaluate(inputs, ground_truths):
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are an expert analyst specializing in {inputs['product_type']} market trends."},
            {"role": "user", "content": f"Could you provide an analysis of the current market performance and consumer reception of {inputs['product_type']} in {inputs['region']}? Please include any notable trends or challenges specific to this region."}
        ]
    )

    # Output -> session output
    return completion.choices[0].message.content

dataset = [
    {
        "inputs": {
            "product_type": "electric vehicles",
            "region": "western europe",
            "time_period": "first half of 2023",
            "metric_1": "total revenue",
            "metric_2": "market share"
        },
        "ground_truths": {
            "response": "As of 2023, the electric vehicle (EV) market in Western Europe is experiencing significant growth, with the region maintaining its status as a global leader in EV adoption. [continue...]",
        }
    },
    {
        "inputs": {
            "product_type": "gaming consoles",
            "region": "north america",
            "time_period": "holiday season 2022",
            "metric_1": "units sold",
            "metric_2": "gross profit margin"
        },
        "ground_truths": {
            "response": "As of 2023, the gaming console market in North America is characterized by intense competition, steady consumer demand, and evolving trends influenced by technological advancements and changing consumer preferences. [continue...]",
        }
    },
    {
        "inputs": {
            "product_type": "smart home devices",
            "region": "australia and new zealand",
            "time_period": "fiscal year 2022-2023",
            "metric_1": "customer acquisition cost",
            "metric_2": "average revenue per user"
        },
        "ground_truths": {
            "response": "As of 2023, the market for smart home devices in Australia and New Zealand is experiencing robust growth, driven by increasing consumer interest in home automation and the enhanced convenience and security these devices offer. [continue...]",
        }
    },
]

@aevaluator()
async def sample_evaluator(outputs, inputs, ground_truths):
    # Simple random score for demonstration
    return random.randint(1, 5)

async def main():
    # Run experiment
    await async_evaluate(
        function=function_to_evaluate,
        hh_api_key=os.environ.get("HONEYHIVE_API_KEY", "your_api_key_here"),
        hh_project=os.environ.get("HONEYHIVE_PROJECT", "your_project_here"),
        name='Sample Experiment',
        dataset=dataset,
        evaluators=[sample_evaluator],
        server_url=os.environ.get("HONEYHIVE_SERVER_URL")  # Optional / Required for self-hosted or dedicated deployments
    )

if __name__ == "__main__":
    asyncio.run(main()) 