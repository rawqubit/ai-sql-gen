import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.argument('description')
@click.option('--schema', help='Optional database schema description.')
def sql_gen(description, schema):
    """AI-powered SQL query generator from natural language."""
    console.print(f"[bold blue]Generating SQL for: {description}...[/bold blue]")

    prompt = f"""
    Translate the following natural language request into an executable SQL query.
    {f"Database Schema: {schema}" if schema else ""}
    Request: {description}
    Format your response in Markdown.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert SQL developer."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        sql_text = response.choices[0].message.content
        console.print(Markdown(sql_text))
    except Exception as e:
        console.print(f"[bold red]Error during SQL generation:[/bold red] {e}")

if __name__ == '__main__':
    sql_gen()
