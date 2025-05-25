*** Settings ***
Library   Browser  plugins=${CURDIR}/AlumniumPlugin.py
Suite Setup  Suite Initialization
*** Variables ***
${AI_PROVIDER}    
${AI_MODEL}    
${AI_API_KEY}    
${URL}    https://seleniumbase.io/apps/calculator

*** Test Cases ***

Do Calculations With AI
    # robotcode: ignore
    New AI Page  ${URL}
    Ai Do   Calculate the sum of 2 + 2. Then Multiply the result by 12 and then divide it by 6"
    AI Check  Result is 8
    Take Screenshot  EMBED  id=output

Do Calculations With BrowserLib
    New Page  ${URL}
    Click  id=2
    Click  id=add
    Click  id=2
    Click  id=equal
    Click  id=multiply
    Click  id=1
    Click  id=2
    Click  id=equal
    Click  id=divide
    Click  id=6
    Click  id=equal
    Get Text  id=output  equals  8  message=Calculation resulted in {value}, expected {expected}
    Take Screenshot  EMBED  id=output


*** Keywords ***

Suite Initialization
    New AI Browser  browser=chromium  headless=False
    ...    ai_provider=${AI_PROVIDER}    
    ...    ai_model=${AI_MODEL}
    ...    api_key=${AI_API_KEY}