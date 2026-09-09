import os

PROJECT_DIR = r"C:\Users\205124067\ecommerce"
STATIC_IMG_DIR = os.path.join(PROJECT_DIR, 'static', 'images')
SVG_DIR = os.path.join(STATIC_IMG_DIR, 'products')
os.makedirs(SVG_DIR, exist_ok=True)

svg_assets = {
    # 1. TitanKey Ultra FIDO2
    "titankey.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="tkMetal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="40%" stop-color="#cbd5e1" />
      <stop offset="70%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#cbd5e1" />
    </linearGradient>
    <linearGradient id="tkBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="25%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="tkGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="30%" stop-color="#f59e0b" />
      <stop offset="70%" stop-color="#fbbf24" />
      <stop offset="100%" stop-color="#b45309" />
    </linearGradient>
    <radialGradient id="tkEmeraldGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#34d399" />
      <stop offset="40%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#059669" stop-opacity="0" />
    </radialGradient>
    <filter id="tkShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.18" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="265" rx="75" ry="14" fill="#0f172a" opacity="0.16" />
  <ellipse cx="200" cy="263" rx="55" ry="9" fill="#0f172a" opacity="0.22" />

  <!-- Device Assembly -->
  <g filter="url(#tkShadow)">
    <!-- USB-C Plug Shroud -->
    <rect x="172" y="30" width="56" height="42" rx="10" fill="url(#tkMetal)" stroke="#64748b" stroke-width="1.2" />
    <rect x="177" y="34" width="46" height="14" rx="4" fill="#0f172a" />
    <!-- Connector Gold Pins inside -->
    <rect x="183" y="38" width="34" height="5" rx="1.5" fill="url(#tkGold)" />

    <!-- Main Chassis -->
    <rect x="135" y="66" width="130" height="180" rx="24" fill="url(#tkBody)" stroke="#475569" stroke-width="1.8" />
    <!-- Inner Bevel Highlight Line -->
    <rect x="140" y="71" width="120" height="170" rx="20" fill="none" stroke="#64748b" stroke-width="1" opacity="0.5" />

    <!-- LED Indicator -->
    <circle cx="200" cy="98" r="8" fill="url(#tkEmeraldGlow)" />
    <circle cx="200" cy="98" r="3" fill="#6ee7b7" />

    <!-- Capacitive Biometric Gold Sensor Ring -->
    <circle cx="200" cy="150" r="34" fill="#0f172a" stroke="url(#tkGold)" stroke-width="3.5" />
    <circle cx="200" cy="150" r="28" fill="none" stroke="url(#tkGold)" stroke-width="1" opacity="0.6" stroke-dasharray="3,2" />
    <circle cx="200" cy="150" r="22" fill="none" stroke="url(#tkGold)" stroke-width="1" opacity="0.4" />
    <circle cx="200" cy="150" r="14" fill="url(#tkGold)" />
    <circle cx="200" cy="150" r="8" fill="#d97706" opacity="0.4" />

    <!-- Precision Lanyard Hole with Brass Eyelet -->
    <circle cx="200" cy="220" r="13" fill="none" stroke="url(#tkMetal)" stroke-width="3" />
    <circle cx="200" cy="220" r="9" fill="#ffffff" opacity="0.95" />
  </g>
</svg>''',

    # 2. AegisVault Pro 1TB Encrypted SSD
    "aegisvault.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="avChassis" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="30%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="avKey" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="avBumper" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <filter id="avShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="18" />
      <feComponentTransfer><feFuncA type="linear" slope="0.2" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="274" rx="90" ry="14" fill="#0f172a" opacity="0.18" />
  <ellipse cx="200" cy="272" rx="65" ry="8" fill="#0f172a" opacity="0.25" />

  <!-- Hard Drive Body -->
  <g filter="url(#avShadow)">
    <!-- Main Aluminum Casing -->
    <rect x="125" y="22" width="150" height="240" rx="16" fill="url(#avChassis)" stroke="#475569" stroke-width="1.8" />
    
    <!-- Top & Bottom Shock Absorber Bumpers -->
    <path d="M125 36 Q125 22 139 22 L261 22 Q275 22 275 36 L275 42 L125 42 Z" fill="url(#avBumper)" />
    <path d="M125 242 L275 242 L275 248 Q275 262 261 262 L139 262 Q125 262 125 248 Z" fill="url(#avBumper)" />

    <!-- Status LED Cluster -->
    <rect x="145" y="48" width="110" height="22" rx="6" fill="#020617" stroke="#1e293b" stroke-width="1" />
    <!-- Red Locked LED -->
    <circle cx="168" cy="59" r="4" fill="#ef4444" />
    <circle cx="168" cy="59" r="7" fill="#ef4444" opacity="0.3" />
    <!-- Amber Standby LED -->
    <circle cx="200" cy="59" r="4" fill="#eab308" />
    <!-- Green Unlocked LED -->
    <circle cx="232" cy="59" r="4" fill="#10b981" />
    <circle cx="232" cy="59" r="7" fill="#10b981" opacity="0.3" />

    <!-- Keypad Matrix (4 rows x 3 columns) -->
    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="700" font-size="12" text-anchor="middle">
      <!-- Row 1 -->
      <g transform="translate(142, 80)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">1</text>
      </g>
      <g transform="translate(184, 80)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">2</text>
      </g>
      <g transform="translate(226, 80)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">3</text>
      </g>
      <!-- Row 2 -->
      <g transform="translate(142, 114)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">4</text>
      </g>
      <g transform="translate(184, 114)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">5</text>
      </g>
      <g transform="translate(226, 114)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">6</text>
      </g>
      <!-- Row 3 -->
      <g transform="translate(142, 148)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">7</text>
      </g>
      <g transform="translate(184, 148)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">8</text>
      </g>
      <g transform="translate(226, 148)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">9</text>
      </g>
      <!-- Row 4 -->
      <g transform="translate(142, 182)">
        <rect width="32" height="26" rx="5" fill="#991b1b" stroke="#f87171" stroke-width="1" />
        <text x="16" y="17" fill="#ffffff" font-size="11">🔒</text>
      </g>
      <g transform="translate(184, 182)">
        <rect width="32" height="26" rx="5" fill="url(#avKey)" stroke="#64748b" stroke-width="1" />
        <text x="16" y="18" fill="#f8fafc">0</text>
      </g>
      <g transform="translate(226, 182)">
        <rect width="32" height="26" rx="5" fill="#065f46" stroke="#34d399" stroke-width="1" />
        <text x="16" y="17" fill="#ffffff" font-size="11">🔓</text>
      </g>
    </g>

    <!-- USB-C Port at bottom -->
    <rect x="184" y="248" width="32" height="8" rx="4" fill="#020617" stroke="#64748b" stroke-width="1" />
  </g>
</svg>''',

    # 3. IronWall Gigabit VPN Router
    "ironwall.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="iwChassis" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="40%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="iwAntenna" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="50%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>
    <filter id="iwShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.22" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="200" cy="268" rx="145" ry="16" fill="#0f172a" opacity="0.18" />
  <ellipse cx="200" cy="265" rx="110" ry="10" fill="#0f172a" opacity="0.24" />

  <g filter="url(#iwShadow)">
    <!-- 3 Adjustable Antennas -->
    <!-- Left Antenna (angled -20 deg) -->
    <g transform="translate(100, 130) rotate(-20)">
      <rect x="-5" y="-115" width="10" height="115" rx="5" fill="url(#iwAntenna)" />
      <circle cx="0" cy="0" r="10" fill="#1e293b" stroke="#64748b" stroke-width="2" />
    </g>
    <!-- Center Antenna (vertical) -->
    <g transform="translate(200, 130)">
      <rect x="-5" y="-120" width="10" height="120" rx="5" fill="url(#iwAntenna)" />
      <circle cx="0" cy="0" r="10" fill="#1e293b" stroke="#64748b" stroke-width="2" />
    </g>
    <!-- Right Antenna (angled +20 deg) -->
    <g transform="translate(300, 130) rotate(20)">
      <rect x="-5" y="-115" width="10" height="115" rx="5" fill="url(#iwAntenna)" />
      <circle cx="0" cy="0" r="10" fill="#1e293b" stroke="#64748b" stroke-width="2" />
    </g>

    <!-- Router Main Chassis -->
    <rect x="65" y="130" width="270" height="110" rx="14" fill="url(#iwChassis)" stroke="#475569" stroke-width="2" />
    <!-- Aluminum Chamfer Edge -->
    <path d="M70 132 L330 132" stroke="#64748b" stroke-width="1.5" />

    <!-- Front Glossy Visor Screen -->
    <rect x="85" y="152" width="230" height="42" rx="8" fill="#020617" stroke="#1e293b" stroke-width="1.5" />
    
    <!-- Status LEDs with Glint -->
    <!-- Power LED -->
    <circle cx="108" cy="173" r="3.5" fill="#10b981" />
    <circle cx="108" cy="173" r="6" fill="#10b981" opacity="0.3" />
    <!-- Internet / WAN LED -->
    <circle cx="132" cy="173" r="3.5" fill="#0284c7" />
    <circle cx="132" cy="173" r="6" fill="#0284c7" opacity="0.3" />
    <!-- LAN 1,2,3,4 LEDs -->
    <circle cx="156" cy="173" r="3" fill="#10b981" />
    <circle cx="174" cy="173" r="3" fill="#10b981" />
    <circle cx="192" cy="173" r="3" fill="#10b981" />
    <circle cx="210" cy="173" r="3" fill="#10b981" />
    <!-- Hardware VPN Active Jewel -->
    <g transform="translate(260, 163)">
      <rect width="40" height="20" rx="4" fill="#064e3b" stroke="#059669" stroke-width="1" />
      <circle cx="12" cy="10" r="3" fill="#34d399" />
      <path d="M22 6 L28 10 L22 14 Z" fill="#34d399" />
    </g>

    <!-- Heat Dissipation Slots -->
    <line x1="110" y1="212" x2="290" y2="212" stroke="#334155" stroke-width="3" stroke-linecap="round" />
    <line x1="130" y1="222" x2="270" y2="222" stroke="#334155" stroke-width="3" stroke-linecap="round" />
  </g>
</svg>''',

    # 4. CipherShield Faraday Laptop Sleeve
    "faraday.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="fsBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="35%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="fsFlap" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="fsLeather" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b45309" />
      <stop offset="100%" stop-color="#78350f" />
    </linearGradient>
    <filter id="fsShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.22" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="200" cy="270" rx="140" ry="16" fill="#0f172a" opacity="0.18" />
  <ellipse cx="200" cy="268" rx="105" ry="10" fill="#0f172a" opacity="0.22" />

  <g filter="url(#fsShadow)">
    <!-- Main Sleeve Body -->
    <rect x="65" y="65" width="270" height="190" rx="16" fill="url(#fsBody)" stroke="#475569" stroke-width="1.8" />
    <!-- Perimeter Double Stitching -->
    <rect x="73" y="73" width="254" height="174" rx="10" fill="none" stroke="#64748b" stroke-width="1.2" stroke-dasharray="4,4" />

    <!-- Magnetic Top Closure Flap -->
    <path d="M65 80 Q65 60 85 60 L315 60 Q335 60 335 80 L325 125 Q200 145 75 125 Z" fill="url(#fsFlap)" stroke="#64748b" stroke-width="1.5" />
    <!-- Flap Double Stitching -->
    <path d="M75 75 L325 75 L317 116 Q200 135 83 116 Z" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4,4" />

    <!-- Silver Conductive Faraday Shield Lip Peek -->
    <line x1="85" y1="124" x2="315" y2="124" stroke="#cbd5e1" stroke-width="2" opacity="0.7" />

    <!-- Leather Pull Tab Accent with Brass Rivet -->
    <g transform="translate(182, 118)">
      <rect width="36" height="28" rx="6" fill="url(#fsLeather)" stroke="#92400e" stroke-width="1" />
      <circle cx="18" cy="14" r="4.5" fill="#f59e0b" stroke="#78350f" stroke-width="1" />
      <circle cx="18" cy="14" r="2" fill="#d97706" />
    </g>

    <!-- Subtle Embossed Geometric Hex Shield Stamp -->
    <path d="M200 175 L218 185 V205 L200 215 L182 205 V185 Z" fill="none" stroke="#334155" stroke-width="2" />
    <path d="M200 183 L210 189 V201 L200 207 L190 201 V189 Z" fill="#1e293b" opacity="0.6" />
  </g>
</svg>''',

    # 5. PrivaShield Cam & Mic Lockdown Pack
    "privashield.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="psMetal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="40%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="psGoldPin" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="50%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>
    <radialGradient id="psLens" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="40%" stop-color="#0284c7" />
      <stop offset="80%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </radialGradient>
    <filter id="psShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" />
      <feOffset dx="0" dy="14" />
      <feComponentTransfer><feFuncA type="linear" slope="0.2" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadows -->
  <ellipse cx="140" cy="245" rx="65" ry="12" fill="#0f172a" opacity="0.18" />
  <ellipse cx="275" cy="255" rx="45" ry="10" fill="#0f172a" opacity="0.18" />

  <g filter="url(#psShadow)">
    <!-- 1. Precision CNC Aluminum Webcam Slider -->
    <g transform="translate(60, 80)">
      <!-- Base Plate -->
      <rect width="170" height="70" rx="35" fill="url(#psMetal)" stroke="#64748b" stroke-width="2" />
      
      <!-- Optical Aperture Hole with Glass Lens -->
      <circle cx="48" cy="35" r="22" fill="#020617" stroke="#334155" stroke-width="2" />
      <circle cx="48" cy="35" r="16" fill="url(#psLens)" />
      <circle cx="44" cy="31" r="4" fill="#ffffff" opacity="0.8" />
      <circle cx="53" cy="39" r="2" fill="#ffffff" opacity="0.5" />

      <!-- Sliding Mechanical Shutter -->
      <rect x="75" y="10" width="85" height="50" rx="25" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
      <!-- Tactile Ridged Thumb Grip -->
      <line x1="110" y1="25" x2="110" y2="45" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="118" y1="25" x2="118" y2="45" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="126" y1="25" x2="126" y2="45" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" />
    </g>

    <!-- 2. Acoustic 3.5mm Mic Blocker Silencer Plug -->
    <g transform="translate(255, 65)">
      <!-- Diamond-Knurled Aluminum Handle -->
      <rect x="0" y="0" width="48" height="65" rx="8" fill="url(#psMetal)" stroke="#64748b" stroke-width="2" />
      <line x1="4" y1="18" x2="44" y2="18" stroke="#475569" stroke-width="1.5" />
      <line x1="4" y1="32" x2="44" y2="32" stroke="#475569" stroke-width="1.5" />
      <line x1="4" y1="46" x2="44" y2="46" stroke="#475569" stroke-width="1.5" />

      <!-- Gold-Plated TRRS 4-Pole 3.5mm Jack Pin -->
      <rect x="16" y="65" width="16" height="110" rx="3" fill="url(#psGoldPin)" />
      <rect x="15" y="85" width="18" height="4" fill="#020617" />
      <rect x="15" y="110" width="18" height="4" fill="#020617" />
      <rect x="15" y="135" width="18" height="4" fill="#020617" />
      <polygon points="16,170 32,170 24,182" fill="url(#psGoldPin)" />
    </g>
  </g>
</svg>''',

    # 6. YubiToken Dual-Interface NFC
    "yubitoken.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="ytBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="30%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0b1120" />
    </linearGradient>
    <linearGradient id="ytGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="40%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>
    <filter id="ytShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.18" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="265" rx="70" ry="14" fill="#0f172a" opacity="0.18" />
  <ellipse cx="200" cy="263" rx="50" ry="8" fill="#0f172a" opacity="0.25" />

  <g filter="url(#ytShadow)">
    <!-- USB-A Metallic Contact Tongue -->
    <rect x="160" y="24" width="80" height="46" rx="4" fill="url(#ytGold)" stroke="#d97706" stroke-width="1.2" />
    <rect x="172" y="30" width="8" height="28" rx="2" fill="#78350f" />
    <rect x="190" y="30" width="8" height="28" rx="2" fill="#78350f" />
    <rect x="204" y="30" width="8" height="28" rx="2" fill="#78350f" />
    <rect x="220" y="30" width="8" height="28" rx="2" fill="#78350f" />

    <!-- Main Token Body -->
    <rect x="140" y="65" width="120" height="185" rx="18" fill="url(#ytBody)" stroke="#475569" stroke-width="1.5" />

    <!-- Printed NFC Radio Loop Antennas -->
    <path d="M180 115 A20 20 0 0 1 220 115" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" />
    <path d="M170 105 A32 32 0 0 1 230 105" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" />
    <path d="M160 95 A44 44 0 0 1 240 95" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" />

    <!-- Smart Card Security Contact Button -->
    <circle cx="200" cy="155" r="24" fill="#020617" stroke="url(#ytGold)" stroke-width="3" />
    <circle cx="200" cy="155" r="14" fill="url(#ytGold)" />
    <!-- Center 'Y' Touch Emblem -->
    <path d="M195 147 L200 155 L205 147 M200 155 V163" fill="none" stroke="#78350f" stroke-width="2.5" stroke-linecap="round" />

    <!-- Keyring Loop at Base -->
    <circle cx="200" cy="220" r="14" fill="none" stroke="url(#ytGold)" stroke-width="3.5" />
    <circle cx="200" cy="220" r="9" fill="#ffffff" opacity="0.95" />
  </g>
</svg>''',

    # 7. DarkShield 256GB Keypad Flash Drive
    "darkshield.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="dsChassis" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="35%" stop-color="#1e293b" />
      <stop offset="70%" stop-color="#334155" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="dsUsb" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="50%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#94a3b8" />
    </linearGradient>
    <filter id="dsShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.2" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadows -->
  <ellipse cx="185" cy="265" rx="55" ry="12" fill="#0f172a" opacity="0.2" />
  <ellipse cx="280" cy="260" rx="35" ry="10" fill="#0f172a" opacity="0.16" />

  <g filter="url(#dsShadow)">
    <!-- USB 3.2 Connector Plug -->
    <rect x="160" y="22" width="50" height="42" rx="4" fill="url(#dsUsb)" stroke="#64748b" stroke-width="1.2" />
    <!-- Blue SuperSpeed USB Tongue -->
    <rect x="170" y="28" width="30" height="8" rx="2" fill="#0284c7" />
    <rect x="172" y="44" width="8" height="10" rx="1" fill="#475569" />
    <rect x="190" y="44" width="8" height="10" rx="1" fill="#475569" />

    <!-- Main Flash Drive Stick -->
    <rect x="145" y="60" width="80" height="190" rx="14" fill="url(#dsChassis)" stroke="#64748b" stroke-width="1.5" />

    <!-- Rubber Grip Ribs -->
    <rect x="145" y="70" width="80" height="6" fill="#0f172a" />
    <rect x="145" y="82" width="80" height="6" fill="#0f172a" />

    <!-- Dual Status LEDs -->
    <circle cx="170" cy="104" r="3.5" fill="#ef4444" />
    <circle cx="200" cy="104" r="3.5" fill="#10b981" />

    <!-- Micro Tactile PIN Buttons (3 columns x 4 rows) -->
    <g fill="#475569" stroke="#334155" stroke-width="1">
      <circle cx="163" cy="128" r="7" /><circle cx="185" cy="128" r="7" /><circle cx="207" cy="128" r="7" />
      <circle cx="163" cy="150" r="7" /><circle cx="185" cy="150" r="7" /><circle cx="207" cy="150" r="7" />
      <circle cx="163" cy="172" r="7" /><circle cx="185" cy="172" r="7" /><circle cx="207" cy="172" r="7" />
      <circle cx="163" cy="194" r="7" fill="#991b1b" /><circle cx="185" cy="194" r="7" /><circle cx="207" cy="194" r="7" fill="#065f46" />
    </g>

    <!-- Base Lanyard Mount -->
    <rect x="175" y="246" width="20" height="12" rx="3" fill="#334155" />
    <circle cx="185" cy="252" r="4" fill="#ffffff" />

    <!-- Detached Waterproof Aluminum Cap Sitting Beside It -->
    <g transform="translate(255, 155)">
      <rect width="50" height="95" rx="10" fill="url(#dsChassis)" stroke="#64748b" stroke-width="1.5" />
      <!-- Red Silicone O-Ring Seal -->
      <rect x="5" y="8" width="40" height="6" rx="3" fill="#ef4444" />
      <line x1="8" y1="35" x2="42" y2="35" stroke="#475569" stroke-width="2" />
      <line x1="8" y1="50" x2="42" y2="50" stroke="#475569" stroke-width="2" />
      <line x1="8" y1="65" x2="42" y2="65" stroke="#475569" stroke-width="2" />
    </g>
  </g>
</svg>''',

    # 8. SentriGate Managed Firewall Appliance
    "sentrigate.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="sgChassis" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="25%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <filter id="sgShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.22" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="265" rx="150" ry="16" fill="#0f172a" opacity="0.2" />

  <g filter="url(#sgShadow)">
    <!-- Top Extruded Aluminum Heatsink Fins -->
    <g stroke="#334155" stroke-width="3" stroke-linecap="round">
      <line x1="60" y1="92" x2="340" y2="92" />
      <line x1="60" y1="98" x2="340" y2="98" />
      <line x1="60" y1="104" x2="340" y2="104" />
      <line x1="60" y1="110" x2="340" y2="110" />
    </g>

    <!-- Main Chassis -->
    <rect x="50" y="112" width="300" height="135" rx="10" fill="url(#sgChassis)" stroke="#64748b" stroke-width="2" />
    <rect x="62" y="125" width="276" height="110" rx="6" fill="#020617" stroke="#1e293b" stroke-width="1.5" />

    <!-- 4 Shielded RJ45 Gigabit Ethernet Ports -->
    <g transform="translate(80, 150)">
      <rect width="32" height="30" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="1.5" />
      <rect x="6" y="8" width="20" height="16" rx="2" fill="#020617" />
      <line x1="9" y1="12" x2="23" y2="12" stroke="#f59e0b" stroke-width="1.5" />
      <circle cx="8" cy="4" r="2" fill="#eab308" />
      <circle cx="24" cy="4" r="2" fill="#10b981" />
    </g>
    <g transform="translate(122, 150)">
      <rect width="32" height="30" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="1.5" />
      <rect x="6" y="8" width="20" height="16" rx="2" fill="#020617" />
      <line x1="9" y1="12" x2="23" y2="12" stroke="#f59e0b" stroke-width="1.5" />
      <circle cx="8" cy="4" r="2" fill="#10b981" />
      <circle cx="24" cy="4" r="2" fill="#10b981" />
    </g>
    <g transform="translate(164, 150)">
      <rect width="32" height="30" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="1.5" />
      <rect x="6" y="8" width="20" height="16" rx="2" fill="#020617" />
      <line x1="9" y1="12" x2="23" y2="12" stroke="#f59e0b" stroke-width="1.5" />
      <circle cx="8" cy="4" r="2" fill="#10b981" />
      <circle cx="24" cy="4" r="2" fill="#10b981" />
    </g>
    <g transform="translate(206, 150)">
      <rect width="32" height="30" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="1.5" />
      <rect x="6" y="8" width="20" height="16" rx="2" fill="#020617" />
      <line x1="9" y1="12" x2="23" y2="12" stroke="#f59e0b" stroke-width="1.5" />
      <circle cx="8" cy="4" r="2" fill="#10b981" />
      <circle cx="24" cy="4" r="2" fill="#10b981" />
    </g>

    <!-- OLED Real-Time Telemetry Screen -->
    <g transform="translate(255, 142)">
      <rect width="68" height="44" rx="4" fill="#064e3b" stroke="#059669" stroke-width="1" />
      <polyline points="6,34 16,30 26,14 36,26 46,18 56,22 62,34" fill="none" stroke="#34d399" stroke-width="1.8" stroke-linecap="round" />
      <circle cx="26" cy="14" r="2" fill="#6ee7b7" />
      <text x="34" y="10" font-family="monospace" font-size="7" font-weight="bold" fill="#a7f3d0" text-anchor="middle">2.5 Gbps</text>
    </g>

    <!-- Illuminated Rocker Power Switch -->
    <g transform="translate(300, 202)">
      <rect width="22" height="16" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1" />
      <rect x="3" y="3" width="16" height="10" rx="1" fill="#ef4444" />
      <circle cx="11" cy="8" r="2" fill="#ffffff" opacity="0.8" />
    </g>
  </g>
</svg>''',

    # 9. BlackHole USB Data Blocker
    "datablocker.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="dbShell" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#0f172a" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.35" />
    </linearGradient>
    <linearGradient id="dbMetal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="50%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#94a3b8" />
    </linearGradient>
    <filter id="dbShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" />
      <feOffset dx="0" dy="14" />
      <feComponentTransfer><feFuncA type="linear" slope="0.2" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="200" cy="265" rx="100" ry="14" fill="#0f172a" opacity="0.18" />

  <g filter="url(#dbShadow)">
    <rect x="80" y="112" width="55" height="76" rx="4" fill="url(#dbMetal)" stroke="#64748b" stroke-width="1.5" />
    <rect x="95" y="125" width="12" height="16" rx="2" fill="#475569" />
    <rect x="95" y="158" width="12" height="16" rx="2" fill="#475569" />

    <!-- Transparent Smoke Housing Body -->
    <rect x="130" y="90" width="140" height="120" rx="16" fill="url(#dbShell)" stroke="#0284c7" stroke-width="2" />

    <!-- Internal Printed Circuit Board -->
    <rect x="142" y="102" width="116" height="96" rx="8" fill="#042f2e" stroke="#059669" stroke-width="1" />

    <!-- Power Rail Traces (Connected) -->
    <line x1="142" y1="120" x2="258" y2="120" stroke="#ef4444" stroke-width="4" stroke-linecap="round" />
    <circle cx="150" cy="120" r="3" fill="#fecaca" />
    <circle cx="250" cy="120" r="3" fill="#fecaca" />
    <line x1="142" y1="180" x2="258" y2="180" stroke="#10b981" stroke-width="4" stroke-linecap="round" />
    <circle cx="150" cy="180" r="3" fill="#a7f3d0" />
    <circle cx="250" cy="180" r="3" fill="#a7f3d0" />

    <!-- Physically Severed Data Traces -->
    <line x1="142" y1="140" x2="182" y2="140" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <line x1="218" y1="140" x2="258" y2="140" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <circle cx="184" cy="140" r="3" fill="#ef4444" />
    <circle cx="216" cy="140" r="3" fill="#ef4444" />
    <line x1="192" y1="135" x2="208" y2="145" stroke="#ef4444" stroke-width="2" />

    <line x1="142" y1="160" x2="182" y2="160" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <line x1="218" y1="160" x2="258" y2="160" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" />
    <circle cx="184" cy="160" r="3" fill="#ef4444" />
    <circle cx="216" cy="160" r="3" fill="#ef4444" />
    <line x1="192" y1="155" x2="208" y2="165" stroke="#ef4444" stroke-width="2" />

    <!-- USB-A Female Socket on Right -->
    <rect x="270" y="116" width="35" height="68" rx="4" fill="url(#dbMetal)" stroke="#64748b" stroke-width="1.5" />
    <rect x="278" y="126" width="18" height="48" rx="2" fill="#020617" />
  </g>
</svg>''',

    # 10. CryptoVault Steel Seed Backup Cassette
    "cryptovault.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="cvSteel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f1f5f9" />
      <stop offset="25%" stop-color="#94a3b8" />
      <stop offset="60%" stop-color="#64748b" />
      <stop offset="85%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="cvTile" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#cbd5e1" />
    </linearGradient>
    <filter id="cvShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.22" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Shadow -->
  <ellipse cx="200" cy="270" rx="125" ry="16" fill="#0f172a" opacity="0.2" />

  <g filter="url(#cvShadow)">
    <rect x="85" y="45" width="230" height="205" rx="12" fill="url(#cvSteel)" stroke="#475569" stroke-width="2.5" />
    <rect x="92" y="52" width="216" height="191" rx="8" fill="none" stroke="#f8fafc" stroke-width="1.2" opacity="0.7" />

    <!-- 4 Countersunk Torx Security Screws -->
    <circle cx="106" cy="66" r="6" fill="#475569" stroke="#94a3b8" stroke-width="1" />
    <path d="M106 63 L106 69 M103 66 L109 66" stroke="#0f172a" stroke-width="1.5" />
    <circle cx="294" cy="66" r="6" fill="#475569" stroke="#94a3b8" stroke-width="1" />
    <path d="M294 63 L294 69 M291 66 L297 66" stroke="#0f172a" stroke-width="1.5" />
    <circle cx="106" cy="229" r="6" fill="#475569" stroke="#94a3b8" stroke-width="1" />
    <path d="M106 226 L106 232 M103 229 L109 229" stroke="#0f172a" stroke-width="1.5" />
    <circle cx="294" cy="229" r="6" fill="#475569" stroke="#94a3b8" stroke-width="1" />
    <path d="M294 226 L294 232 M291 229 L297 229" stroke="#0f172a" stroke-width="1.5" />

    <!-- Precision Milled Tile Slots with Stamped Steel Letter Tiles -->
    <g font-family="monospace" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">
      <!-- Row 1: Word 01 -->
      <text x="120" y="98" font-size="9" fill="#334155">01</text>
      <rect x="135" y="85" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="144" y="98">A</text>
      <rect x="156" y="85" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="165" y="98">B</text>
      <rect x="177" y="85" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="186" y="98">A</text>
      <rect x="198" y="85" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="207" y="98">N</text>
      <rect x="222" y="85" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />
      <rect x="243" y="85" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />

      <!-- Row 2: Word 02 -->
      <text x="120" y="128" font-size="9" fill="#334155">02</text>
      <rect x="135" y="115" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="144" y="128">C</text>
      <rect x="156" y="115" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="165" y="128">I</text>
      <rect x="177" y="115" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="186" y="128">P</text>
      <rect x="198" y="115" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="207" y="128">H</text>
      <rect x="222" y="115" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />
      <rect x="243" y="115" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />

      <!-- Row 3: Word 03 -->
      <text x="120" y="158" font-size="9" fill="#334155">03</text>
      <rect x="135" y="145" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="144" y="158">S</text>
      <rect x="156" y="145" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="165" y="158">H</text>
      <rect x="177" y="145" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="186" y="158">I</text>
      <rect x="198" y="145" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="207" y="158">E</text>
      <rect x="222" y="145" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />
      <rect x="243" y="145" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />

      <!-- Row 4: Word 04 -->
      <text x="120" y="188" font-size="9" fill="#334155">04</text>
      <rect x="135" y="175" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="144" y="188">Z</text>
      <rect x="156" y="175" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="165" y="188">E</text>
      <rect x="177" y="175" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="186" y="188">R</text>
      <rect x="198" y="175" width="18" height="18" rx="2" fill="url(#cvTile)" stroke="#64748b" /><text x="207" y="188">O</text>
      <rect x="222" y="175" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />
      <rect x="243" y="175" width="18" height="18" rx="2" fill="#334155" stroke="#64748b" />
    </g>
  </g>
</svg>''',

    # 11. AirGate Zero-Trust Cold Wallet
    "airgate.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="agBody" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="35%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="agScreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <filter id="agShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.22" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="272" rx="85" ry="14" fill="#0f172a" opacity="0.2" />

  <g filter="url(#agShadow)">
    <!-- Main Handheld Enclosure -->
    <rect x="130" y="25" width="140" height="235" rx="20" fill="url(#agBody)" stroke="#64748b" stroke-width="1.8" />
    
    <!-- Top Air-Gapped Optical Camera Scanner Lens -->
    <circle cx="200" cy="42" r="7" fill="#020617" stroke="#475569" stroke-width="1.5" />
    <circle cx="200" cy="42" r="3.5" fill="#4f46e5" />
    <circle cx="199" cy="41" r="1" fill="#ffffff" />

    <!-- Color LCD Screen Display with Glass Reflection -->
    <rect x="145" y="60" width="110" height="120" rx="8" fill="url(#agScreen)" stroke="#1e293b" stroke-width="1.5" />
    
    <!-- Screen Header -->
    <rect x="145" y="60" width="110" height="18" rx="6" fill="#0f172a" />
    <text x="200" y="73" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="700" fill="#38bdf8" text-anchor="middle">SIGN TRANSACTION</text>

    <!-- Animated Dynamic Signing QR Matrix -->
    <g fill="#f8fafc">
      <!-- Top-Left Target -->
      <rect x="156" y="86" width="22" height="22" rx="2" />
      <rect x="160" y="90" width="14" height="14" fill="#020617" />
      <rect x="163" y="93" width="8" height="8" />

      <!-- Top-Right Target -->
      <rect x="222" y="86" width="22" height="22" rx="2" />
      <rect x="226" y="90" width="14" height="14" fill="#020617" />
      <rect x="229" y="93" width="8" height="8" />

      <!-- Bottom-Left Target -->
      <rect x="156" y="136" width="22" height="22" rx="2" />
      <rect x="160" y="140" width="14" height="14" fill="#020617" />
      <rect x="163" y="143" width="8" height="8" />

      <!-- QR Payload Data Matrix -->
      <rect x="186" y="86" width="6" height="6" /><rect x="202" y="86" width="8" height="6" />
      <rect x="194" y="96" width="14" height="6" /><rect x="186" y="106" width="8" height="8" />
      <rect x="204" y="106" width="10" height="6" /><rect x="222" y="116" width="6" height="12" />
      <rect x="186" y="122" width="12" height="6" /><rect x="206" y="122" width="8" height="8" />
      <rect x="186" y="136" width="6" height="14" /><rect x="200" y="144" width="12" height="6" />
      <rect x="222" y="136" width="10" height="14" />
    </g>

    <!-- Screen Glass Sheen Diagonal Glare -->
    <polygon points="145,60 190,60 155,180 145,180" fill="#ffffff" opacity="0.04" />

    <!-- Directional Navigation Keypad (D-Pad) -->
    <g transform="translate(178, 195)">
      <rect x="15" y="0" width="14" height="44" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1" />
      <rect x="0" y="15" width="44" height="14" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1" />
      <circle cx="22" cy="22" r="8" fill="#4f46e5" stroke="#818cf8" stroke-width="1" />
      <circle cx="22" cy="22" r="4" fill="#ffffff" />
    </g>
  </g>
</svg>''',

    # 12. TorBouncer Portable Privacy Router
    "torbouncer.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="tbShell" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="40%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#e2e8f0" />
    </linearGradient>
    <linearGradient id="tbScreen" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#020617" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <filter id="tbShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" />
      <feOffset dx="0" dy="16" />
      <feComponentTransfer><feFuncA type="linear" slope="0.18" /></feComponentTransfer>
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Ground Contact Shadow -->
  <ellipse cx="200" cy="265" rx="100" ry="14" fill="#0f172a" opacity="0.16" />
  <ellipse cx="200" cy="262" rx="75" ry="9" fill="#0f172a" opacity="0.22" />

  <g filter="url(#tbShadow)">
    <rect x="110" y="65" width="180" height="175" rx="30" fill="url(#tbShell)" stroke="#cbd5e1" stroke-width="2" />
    <rect x="116" y="71" width="168" height="163" rx="25" fill="none" stroke="#e2e8f0" stroke-width="1.5" />

    <!-- Top Port Cutouts -->
    <g transform="translate(145, 57)">
      <rect width="36" height="12" rx="3" fill="#334155" stroke="#64748b" stroke-width="1" />
      <rect x="6" y="3" width="24" height="6" rx="2" fill="#020617" />
    </g>
    <g transform="translate(200, 57)">
      <rect width="55" height="12" rx="3" fill="#334155" stroke="#64748b" stroke-width="1" />
      <rect x="10" y="3" width="35" height="6" rx="2" fill="#020617" />
    </g>

    <!-- OLED Status Display Screen -->
    <rect x="135" y="95" width="130" height="75" rx="10" fill="url(#tbScreen)" stroke="#334155" stroke-width="1.5" />
    
    <!-- Tor Multi-Hop Onion Circuit Graphic -->
    <g transform="translate(155, 120)">
      <circle cx="20" cy="18" r="14" fill="none" stroke="#a855f7" stroke-width="2" />
      <ellipse cx="20" cy="18" rx="8" ry="14" fill="none" stroke="#a855f7" stroke-width="1.5" />
      <ellipse cx="20" cy="18" rx="3" ry="14" fill="none" stroke="#a855f7" stroke-width="1.2" />
      <circle cx="20" cy="18" r="2.5" fill="#c084fc" />
    </g>

    <!-- Circuit Hops Indicator -->
    <g transform="translate(200, 126)">
      <circle cx="6" cy="12" r="3" fill="#34d399" />
      <line x1="9" y1="12" x2="21" y2="12" stroke="#34d399" stroke-width="1.5" />
      <circle cx="24" cy="12" r="3" fill="#34d399" />
      <line x1="27" y1="12" x2="39" y2="12" stroke="#34d399" stroke-width="1.5" />
      <circle cx="42" cy="12" r="3" fill="#34d399" />
    </g>

    <!-- Signal & Battery Pinpoint LEDs -->
    <g transform="translate(145, 195)">
      <rect width="24" height="12" rx="3" fill="none" stroke="#64748b" stroke-width="1.5" />
      <rect x="2" y="2" width="16" height="8" rx="1" fill="#10b981" />
      <rect x="24" y="3" width="2" height="6" fill="#64748b" />
    </g>
    <g transform="translate(235, 194)">
      <path d="M0 12 A10 10 0 0 1 14 12" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" />
      <path d="M-4 7 A16 16 0 0 1 18 7" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" />
      <circle cx="7" cy="13" r="1.5" fill="#0284c7" />
    </g>
  </g>
</svg>'''
}

# Write SVGs to static/images/products/
for filename, content in svg_assets.items():
    dest_product = os.path.join(SVG_DIR, filename)
    with open(dest_product, 'w', encoding='utf-8') as f:
        f.write(content.strip())

print(f"Successfully generated {len(svg_assets)} realistic product images in {SVG_DIR}")
