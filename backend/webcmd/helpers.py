import json

def generate_safe_fill_script(url: str, safe_field_map: dict) -> str:
    fields_json = json.dumps(safe_field_map)
    return f"""
await page.goto('{url}', {{ waitUntil: 'domcontentloaded', timeout: 25000 }});
await page.waitForTimeout(1000);

const fieldData = {fields_json};
const filledLog = [];
const skippedSensitive = [];

for (const [key, value] of Object.entries(fieldData)) {{
    try {{
        let loc = page.getByLabel(new RegExp(key, 'i'));
        let count = await loc.count();
        
        if (count === 0) {{
            loc = page.locator(`input[name*="${{key}}" i], textarea[name*="${{key}}" i], select[name*="${{key}}" i], #${{key}}`);
            count = await loc.count();
        }}
        
        if (count > 0) {{
            const first = loc.first();
            const inputType = (await first.getAttribute('type') || 'text').toLowerCase();
            
            if (['password', 'hidden'].includes(inputType) || /card|cvv|ssn|pin|pass/i.test(key)) {{
                skippedSensitive.push({{ field: key, reason: 'Sensitive security protection' }});
                continue;
            }}
            
            await first.fill(String(value));
            filledLog.push({{ field: key, value: String(value), status: 'SAFE_FILLED_BY_WEBCMD' }});
        }}
    }} catch (err) {{
        console.log('Error filling field ' + key + ': ' + err);
    }}
}}

const submitBtn = page.getByRole('button', {{ name: /submit|apply now|complete/i }});
const submitDetected = (await submitBtn.count()) > 0;

return {{
    url: page.url(),
    filledFields: filledLog,
    skippedSensitive: skippedSensitive,
    submitButtonDetected: submitDetected,
    haltedForApproval: true
}};
"""