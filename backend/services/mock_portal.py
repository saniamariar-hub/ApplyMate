from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/demo-portal", tags=["Mock Portal"])

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def demo_portal_home():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Global NextGen STEM Scholars Program 2026</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen">
  <header class="bg-gradient-to-r from-blue-900 to-indigo-800 text-white py-8 px-6 shadow-md">
    <div class="max-w-4xl mx-auto flex justify-between items-center">
      <div>
        <span class="bg-blue-500 text-xs font-semibold uppercase px-2.5 py-1 rounded-full text-white tracking-wide">Official Application Portal</span>
        <h1 class="text-3xl font-bold mt-2">Global NextGen STEM Scholars Program 2026</h1>
        <p class="text-blue-100 text-sm mt-1">Hosted by Future Innovators Foundation • Academic Year 2026-2027</p>
      </div>
      <a href="/demo-portal/apply" class="bg-emerald-500 hover:bg-emerald-600 text-white font-medium px-5 py-2.5 rounded-lg shadow transition">
        Apply Now &rarr;
      </a>
    </div>
  </header>

  <main class="max-w-4xl mx-auto py-8 px-6 space-y-8">
    <div class="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg shadow-sm flex items-start space-x-3">
      <div class="text-amber-600 text-xl font-bold">⏱</div>
      <div>
        <h3 class="font-semibold text-amber-900">Application Deadline: October 15, 2026 at 23:59 PST</h3>
        <p class="text-sm text-amber-800">Applications submitted after the deadline will not be evaluated. Early submissions are encouraged.</p>
      </div>
    </div>

    <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 class="text-xl font-bold text-slate-900 border-b pb-2">Program Overview</h2>
      <p class="text-slate-600 leading-relaxed">
        The Global NextGen STEM Scholars Program provides up to <strong>$15,000 USD</strong> in tuition support, research mentorship, and industry networking for high-achieving undergraduate students pursuing degrees in Computer Science, Data Science, Artificial Intelligence, and related Engineering disciplines.
      </p>
    </section>

    <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 class="text-xl font-bold text-slate-900 border-b pb-2">Eligibility Criteria</h2>
      <ul class="space-y-2.5 text-slate-700">
        <li class="flex items-start">
          <span class="text-emerald-600 font-bold mr-2">✓</span>
          <span><strong>Academic Standing:</strong> Currently enrolled full-time undergraduate student in Year 2 (Sophomore) or Year 3 (Junior).</span>
        </li>
        <li class="flex items-start">
          <span class="text-emerald-600 font-bold mr-2">✓</span>
          <span><strong>Minimum GPA:</strong> Cumulative GPA of <strong>3.50 or higher</strong> on a 4.0 scale (or equivalent >= 85%).</span>
        </li>
        <li class="flex items-start">
          <span class="text-emerald-600 font-bold mr-2">✓</span>
          <span><strong>Qualifying Majors:</strong> Computer Science, Data Science, Software Engineering, Electrical Engineering, Applied Mathematics.</span>
        </li>
        <li class="flex items-start">
          <span class="text-emerald-600 font-bold mr-2">✓</span>
          <span><strong>Financial Need / Income Cap:</strong> Annual household adjusted gross income below <strong>$75,000 USD</strong>.</span>
        </li>
        <li class="flex items-start">
          <span class="text-emerald-600 font-bold mr-2">✓</span>
          <span><strong>Citizenship:</strong> Open to US Citizens, Permanent Residents, and International Students studying in accredited universities.</span>
        </li>
      </ul>
    </section>

    <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
      <h2 class="text-xl font-bold text-slate-900 border-b pb-2">Mandatory Required Documents</h2>
      <div class="grid md:grid-cols-2 gap-4">
        <div class="p-3.5 bg-slate-50 border rounded-lg">
          <div class="font-semibold text-slate-800">1. Official Academic Transcript</div>
          <div class="text-xs text-slate-500 mt-1">Must show coursework through Spring 2026 and cumulative GPA.</div>
        </div>
        <div class="p-3.5 bg-slate-50 border rounded-lg">
          <div class="font-semibold text-slate-800">2. Proof of Identity / Passport</div>
          <div class="text-xs text-slate-500 mt-1">Valid government passport or national photo ID card.</div>
        </div>
        <div class="p-3.5 bg-slate-50 border rounded-lg">
          <div class="font-semibold text-slate-800">3. Income Certificate / Tax Summary</div>
          <div class="text-xs text-slate-500 mt-1">Recent family tax assessment or official income verification.</div>
        </div>
        <div class="p-3.5 bg-slate-50 border rounded-lg">
          <div class="font-semibold text-slate-800">4. Letter of Recommendation</div>
          <div class="text-xs text-slate-500 mt-1">From a university professor or research supervisor.</div>
        </div>
        <div class="p-3.5 bg-slate-50 border rounded-lg md:col-span-2">
          <div class="font-semibold text-slate-800">5. Statement of Purpose (500 words max)</div>
          <div class="text-xs text-slate-500 mt-1">Explain your research goals, technical aspirations, and community impact.</div>
        </div>
      </div>
    </section>

    <div class="text-center py-6">
      <a href="/demo-portal/apply" class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg px-8 py-3.5 rounded-xl shadow-lg transition">
        Proceed to Online Application Form &rarr;
      </a>
    </div>
  </main>
</body>
</html>"""
    return HTMLResponse(content=html)

@router.get("/apply", response_class=HTMLResponse)
async def demo_portal_apply():
    from backend.services.profile_service import ProfileService
    ps = ProfileService()
    profile = ps.get_profile()
    
    personal = profile.get("personal", {})
    academic = profile.get("academic", {})
    
    first_name = personal.get("first_name", "Aarohi")
    last_name = personal.get("last_name", "Nair")
    email = personal.get("email", "aarohi.nair.demo@example.com")
    phone = personal.get("phone", "+91 98765 43210")
    institution = academic.get("current_institution", "Christ University")
    major = academic.get("major", "Computer Science and Engineering (Artificial Intelligence & Machine Learning)")
    gpa = str(academic.get("gpa", "9.1"))
    sop = "I am applying for this opportunity to further my academic and research endeavors in agentic AI, machine learning, and secure intelligent systems as a computer science undergraduate."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Application Form - Global NextGen STEM Scholars</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 text-slate-800 font-sans min-h-screen py-8 px-4">
  <div class="max-w-2xl mx-auto bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden">
    <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-blue-800 text-white p-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs font-semibold uppercase px-2.5 py-0.5 rounded-full tracking-wide">
            Pre-filled Portal
          </span>
          <h1 class="text-2xl font-bold mt-2">Online Application Form</h1>
          <p class="text-blue-200 text-xs mt-1">Global NextGen STEM Scholars Program 2026 • Program ID: STEM-2026-US</p>
        </div>
        <div class="text-right hidden sm:block">
          <div class="text-xs text-blue-200">Candidate</div>
          <div class="text-sm font-bold text-white">{first_name} {last_name}</div>
        </div>
      </div>
    </div>

    <!-- Banner explaining pre-fill status -->
    <div class="bg-emerald-50 border-b border-emerald-200 p-4 flex items-center gap-3 text-xs text-emerald-900">
      <div class="w-6 h-6 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-sm shrink-0">✓</div>
      <div>
        <strong>Pre-fill Completed:</strong> Safe profile parameters have been populated directly from your <strong>Student Vault</strong>. Review each field below before manual submission.
      </div>
    </div>

    <form id="scholarshipForm" class="p-6 space-y-6" onsubmit="event.preventDefault(); document.getElementById('successModal').classList.remove('hidden');">
      <!-- 1. Candidate Information -->
      <div class="space-y-4">
        <h3 class="text-base font-bold text-slate-900 border-b pb-1">1. Candidate Information</h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="first_name" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">First Name</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="text" id="first_name" name="first_name" value="{first_name}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="last_name" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Last Name</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="text" id="last_name" name="last_name" value="{last_name}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="email" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Email Address</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="email" id="email" name="email" value="{email}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="phone" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Phone Number</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="tel" id="phone" name="phone" value="{phone}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <!-- 2. Academic Background -->
      <div class="space-y-4">
        <h3 class="text-base font-bold text-slate-900 border-b pb-1">2. Academic Background</h3>
        
        <div>
          <div class="flex items-center justify-between mb-1">
            <label for="current_institution" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Current University / College</label>
            <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
              ✓ Pre-filled from Student Vault
            </span>
          </div>
          <input type="text" id="current_institution" name="current_institution" value="{institution}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="major" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Degree Major</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="text" id="major" name="major" value="{major}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1">
              <label for="gpa" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Cumulative GPA</label>
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
                ✓ Pre-filled from Student Vault
              </span>
            </div>
            <input type="text" id="gpa" name="gpa" value="{gpa}" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none" required />
          </div>
        </div>
      </div>

      <!-- 3. Personal Statement -->
      <div class="space-y-2">
        <div class="flex items-center justify-between mb-1">
          <label for="statement_of_purpose" class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Statement of Purpose / Essay</label>
          <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-100 border border-emerald-300 px-1.5 py-0.5 rounded">
            ✓ Pre-filled from Student Vault
          </span>
        </div>
        <textarea id="statement_of_purpose" name="statement_of_purpose" rows="4" class="w-full border border-emerald-400 bg-emerald-50/20 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none">{sop}</textarea>
      </div>

      <!-- Safety Guard Notice -->
      <div class="p-3.5 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-900 flex items-start gap-2.5">
        <span class="text-base">🛡️</span>
        <div>
          <strong>Human Approval Guard:</strong> The Application Readiness Agent has safely mapped and populated your credentials. The submission boundary is strictly maintained—automated submission without candidate review is prohibited.
        </div>
      </div>

      <!-- Form Actions -->
      <div class="pt-4 flex justify-between items-center border-t">
        <a href="/demo-portal" class="text-xs text-slate-500 hover:text-slate-700">&larr; Back to Program Overview</a>
        <button type="submit" id="submit_application_btn" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm px-6 py-2.5 rounded-lg shadow-md hover:shadow-lg transition flex items-center gap-2">
          <span>Submit Verified Application</span>
          <span>&rarr;</span>
        </button>
      </div>
    </form>
  </div>

  <!-- Success Modal -->
  <div id="successModal" class="hidden fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 text-center shadow-2xl border border-slate-200 space-y-4">
      <div class="w-14 h-14 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto text-2xl font-bold">
        ✓
      </div>
      <h3 class="text-xl font-bold text-slate-900">Application Submitted!</h3>
      <p class="text-xs text-slate-600 leading-relaxed">
        Your application for <strong>Global NextGen STEM Scholars Program 2026</strong> has been successfully submitted after candidate review and approval.
      </p>
      <div class="pt-2">
        <button onclick="document.getElementById('successModal').classList.add('hidden')" class="w-full bg-slate-900 text-white font-semibold text-xs py-2.5 rounded-lg hover:bg-slate-800 transition">
          Close Window
        </button>
      </div>
    </div>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)