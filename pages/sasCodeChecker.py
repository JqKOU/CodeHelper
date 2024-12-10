import streamlit as st
import re

# Function to check SAS code syntax
def sas_syntax_checker(sas_code):
    issues = {
        "missing_semicolons": [],
        "unmatched_parentheses": [],
        "unmatched_quotes": [],
        "unclosed_comments": [],
        "unmatched_do_end": [],
        "missing_run_quit": [],
        "long_lines": []
    }
    
    # Split the SAS code into lines
    lines = sas_code.split("\n")
    
    # Initialize counters and flags
    parentheses_count = 0
    quote_flag = False
    comment_flag = False
    do_count = 0
    open_blocks = []
    last_proc_or_data = None

    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        
        # Check for missing semicolons
        if stripped_line and not stripped_line.endswith(";") and not stripped_line.startswith(("*", "%", "/*")):
            issues["missing_semicolons"].append((line_number, line))
        
        # Check for unmatched parentheses
        parentheses_count += line.count("(") - line.count(")")
        
        # Check for unmatched quotes
        quote_flag ^= line.count("'") % 2  # Toggle flag if odd number of single quotes
        quote_flag ^= line.count('"') % 2  # Toggle flag if odd number of double quotes
        
        # Check for unclosed comments
        comment_flag ^= stripped_line.count("/*") > stripped_line.count("*/")
        
        # Check for unmatched DO-END blocks
        if re.match(r'^\s*do\b', stripped_line, re.IGNORECASE):
            do_count += 1
            open_blocks.append(("DO", line_number))
        elif re.match(r'^\s*end\b', stripped_line, re.IGNORECASE):
            do_count -= 1
            if open_blocks and open_blocks[-1][0] == "DO":
                open_blocks.pop()
        
        # Track PROC or DATA steps for missing RUN or QUIT
        if re.match(r'^\s*(proc|data)\b', stripped_line, re.IGNORECASE):
            last_proc_or_data = line_number
        if re.match(r'^\s*(run|quit)\b', stripped_line, re.IGNORECASE):
            last_proc_or_data = None
        
        # Check for long lines
        if len(line) > 80:
            issues["long_lines"].append((line_number, line))
    
    # Final unmatched checks
    if parentheses_count != 0:
        issues["unmatched_parentheses"].append(f"Unmatched parentheses found ({parentheses_count} remaining).")
    if quote_flag:
        issues["unmatched_quotes"].append("Unmatched quotes found in the file.")
    if comment_flag:
        issues["unclosed_comments"].append("Unclosed comment block found in the file.")
    if do_count != 0:
        issues["unmatched_do_end"].append(f"Unmatched DO-END blocks ({do_count} remaining).")
    if last_proc_or_data is not None:
        issues["missing_run_quit"].append(f"PROC or DATA step starting at line {last_proc_or_data} is not terminated with RUN or QUIT.")
    
    return issues


# Streamlit App
def main():
    st.title("SAS Syntax Checker")
    st.write("Enter your SAS code below to check for syntax issues.")
    
    # Text area for SAS code input
    sas_code = st.text_area("SAS Code", height=300, placeholder="Enter your SAS code here...")
    
    # Button to trigger the syntax check
    if st.button("Check Syntax"):
        if not sas_code.strip():
            st.warning("Please enter SAS code before checking.")
        else:
            issues = sas_syntax_checker(sas_code)
            
            # Display results
            for issue_type, details in issues.items():
                st.subheader(issue_type.replace("_", " ").title())
                if details:
                    for detail in details:
                        if isinstance(detail, tuple):
                            st.write(f"Line {detail[0]}: {detail[1]}")
                        else:
                            st.write(detail)
                else:
                    st.write("No issues found.")

if __name__ == "__main__":
    main()
