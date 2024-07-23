import argparse
import pandas as pd
import random

# argument parser
parser = argparse.ArgumentParser(
    prog="Needle in a Haystack Dataset Generator",
    description="Uses a list of documents to generate needle in a haystack tests for RAG evaluations",
)
parser.add_argument('-f', '--files', nargs='+', default= 'paul_graham_essays.csv')
parser.add_argument('-c', '--copies', type=int, default=4)
args = parser.parse_args()

WORDS = [
    "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", 
    "Golf", "Hotel", "India", "Juliett", "Kilo", "Leapfrog", 
    "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", 
    "Sierra", "Tango", "Unicorn", "Victor", "Whiskey", 
    "Xray", "Yankee", "Zulu"
]

essays = pd.read_csv(args.files)
depths = [0.0, 0.25, 0.50, 0.75, 1.0]
lengths = [512, 1024, 4096, 8192, 16384, 32768]
copies = args.copies
total_copies = len(depths) * len(lengths) * copies


def generate_niah_dataset(): 
    print("Beginning dataset generation")
    df = pd.DataFrame(columns=['context_length', 'context_depth', 'secret_code', 'copy', 'context'])
    counter = 0
    for length in lengths:
        for depth in depths:
            for ii in range(copies):
                context = sample_df_for_length(df=essays, length=length)
                context_point = find_nearest_left_period(context, depth)
                insert_point = context_point if context_point >=0 else 0
                secret_code = random.choice(WORDS) + str(random.randint(100,999))
                code_string = f"Doug's secret code is: {secret_code}. Remember this."
                if depth == 1.0:
                    code_string = " " + code_string
                else:
                    code_string = code_string + " "
                new_context = ''.join((context[:insert_point],code_string,context[insert_point:]))
                df.loc[counter] = [length, depth, secret_code, ii, new_context]
                counter += 1
        print(f"Added row {counter} out of {total_copies}")
    df.to_json("LFAI_RAG_niah_q1.json",orient="records", lines=True)


def sample_df_for_length(df, length):
    sample = ''
    while len(sample) < length:
        sample += df['text'].sample(n=1).values[0]

    while len(sample) > (length - 60):
        sample = sample[0:sample[:-1].rfind('.')+1]

    return sample    

def find_nearest_left_period(text, depth):
    depth_index = int(len(text) * depth)

    current_index = depth_index - 1
    
    if depth == 0:
        return 0

    while current_index > 0:
        if current_index > 0 and text[current_index] == '.':
            return current_index + 2
        current_index -= 1
    
    # If no period is found, return 0 (use beginning of the string)
    return 0

if __name__=="__main__":
    generate_niah_dataset()