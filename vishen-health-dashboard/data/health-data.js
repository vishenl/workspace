// Vishen's Complete Health Data
const healthData = {
  patient: {
    name: "Vishen Lakhiani",
    age: 49,
    gender: "Male",
    lastUpdated: "November 2025"
  },

  healthScores: {
    overall: 84,
    categories: {
      testosterone: { score: 62, status: "needs-optimization", color: "#F59E0B" },
      cardiovascular: { score: 71, status: "moderate", color: "#EF4444" },
      cognitive: { score: 88, status: "excellent", color: "#10B981" },
      energy: { score: 92, status: "excellent", color: "#10B981" },
      vision: { score: 45, status: "needs-attention", color: "#EF4444" },
      sleep: { score: 85, status: "good", color: "#10B981" }
    }
  },

  bloodWork: {
    critical: [
      {
        name: "SHBG",
        value: 66.9,
        unit: "nmol/L",
        optimal: { min: 20, max: 40 },
        reference: { min: 10, max: 57 },
        status: "high",
        concern: "High SHBG binds testosterone, reducing bioavailability",
        priority: "high"
      },
      {
        name: "LDL Cholesterol",
        value: 171,
        unit: "mg/dL",
        optimal: { min: 70, max: 100 },
        reference: { min: 0, max: 130 },
        status: "high",
        concern: "Elevated cardiovascular risk",
        priority: "high"
      },
      {
        name: "Free Testosterone",
        value: 23.9,
        unit: "pg/mL",
        optimal: { min: 35, max: 155 },
        reference: { min: 15, max: 50 },
        status: "borderline",
        concern: "Lower side of optimal range",
        priority: "medium"
      }
    ],
    excellent: [
      {
        name: "HbA1c",
        value: 4.9,
        unit: "%",
        optimal: { min: 4.0, max: 5.6 },
        reference: { min: 4.0, max: 5.6 },
        status: "excellent",
        concern: "Excellent glucose control"
      },
      {
        name: "CRP",
        value: 0.5,
        unit: "mg/L",
        optimal: { min: 0, max: 1 },
        reference: { min: 0, max: 3 },
        status: "excellent",
        concern: "Low inflammation"
      },
      {
        name: "Vitamin D",
        value: 41.8,
        unit: "ng/mL",
        optimal: { min: 40, max: 60 },
        reference: { min: 30, max: 100 },
        status: "excellent",
        concern: "Optimal levels"
      },
      {
        name: "Ferritin",
        value: 220,
        unit: "ng/mL",
        optimal: { min: 100, max: 300 },
        reference: { min: 30, max: 400 },
        status: "excellent",
        concern: "Good iron stores"
      }
    ],
    borderline: [
      {
        name: "HDL Cholesterol",
        value: 51,
        unit: "mg/dL",
        optimal: { min: 60, max: 100 },
        reference: { min: 40, max: 100 },
        status: "borderline",
        concern: "Could be higher for cardiovascular protection"
      }
    ]
  },

  projections: {
    timeline: ["Current", "3 Months", "6 Months"],
    biomarkers: [
      {
        name: "SHBG",
        values: [66.9, 45, 38],
        optimal: 35,
        unit: "nmol/L"
      },
      {
        name: "LDL",
        values: [171, 130, 110],
        optimal: 90,
        unit: "mg/dL"
      },
      {
        name: "Free Testosterone",
        values: [23.9, 38, 42],
        optimal: 45,
        unit: "pg/mL"
      },
      {
        name: "HDL",
        values: [51, 58, 65],
        optimal: 65,
        unit: "mg/dL"
      }
    ]
  },

  supplements: {
    current: {
      count: 35,
      monthlyCost: 450,
      items: [
        { name: "Whey Protein", category: "performance", action: "keep", priority: "high" },
        { name: "Creatine Monohydrate", category: "performance", action: "keep", priority: "high" },
        { name: "Omega-3 (Fish Oil)", category: "cardiovascular", action: "keep", priority: "high" },
        { name: "Vitamin D3", category: "hormones", action: "keep", priority: "high" },
        { name: "Magnesium Glycinate", category: "recovery", action: "keep", priority: "high" },
        { name: "Zinc", category: "hormones", action: "keep", priority: "medium" },
        { name: "Ashwagandha", category: "stress", action: "keep", priority: "medium" },
        { name: "Rhodiola", category: "energy", action: "keep", priority: "medium" },
        { name: "CoQ10", category: "energy", action: "keep", priority: "medium" },
        { name: "B-Complex", category: "energy", action: "keep", priority: "medium" },
        { name: "Vitamin C", category: "immune", action: "keep", priority: "low" },
        { name: "Probiotics", category: "gut", action: "keep", priority: "medium" },
        { name: "Collagen", category: "recovery", action: "keep", priority: "low" },
        { name: "Multivitamin", category: "general", action: "remove", priority: "low", reason: "Redundant with targeted supplements" },
        { name: "Glucosamine", category: "joints", action: "modify", priority: "low", recommendation: "Switch to MSM + Collagen Type II" },
        { name: "Generic Antioxidant", category: "general", action: "remove", priority: "low", reason: "Replace with targeted compounds" },
        { name: "Melatonin", category: "sleep", action: "modify", priority: "low", recommendation: "Reduce dose, use cyclically" },
        { name: "Caffeine Pills", category: "energy", action: "remove", priority: "low", reason: "Use coffee instead" },
        { name: "Random Herbal Blend", category: "general", action: "remove", priority: "low", reason: "Unproven efficacy" }
      ]
    },
    optimized: {
      count: 40,
      monthlyCost: 430,
      additions: [
        { name: "Boron", category: "hormones", reason: "Lower SHBG, boost free testosterone", priority: "high", cost: 12 },
        { name: "Stinging Nettle Root", category: "hormones", reason: "Reduce SHBG binding", priority: "high", cost: 18 },
        { name: "Tongkat Ali", category: "hormones", reason: "Testosterone optimization", priority: "high", cost: 35 },
        { name: "Red Yeast Rice", category: "cardiovascular", reason: "Natural statin for LDL", priority: "high", cost: 25 },
        { name: "Bergamot", category: "cardiovascular", reason: "Improve lipid profile", priority: "high", cost: 28 },
        { name: "Lutein + Zeaxanthin", category: "vision", reason: "Macular protection", priority: "high", cost: 22 },
        { name: "Astaxanthin", category: "vision", reason: "Eye health, reduce fatigue", priority: "high", cost: 30 },
        { name: "Bilberry Extract", category: "vision", reason: "Night vision, eye circulation", priority: "medium", cost: 20 },
        { name: "NAC", category: "detox", reason: "Liver support, glutathione", priority: "medium", cost: 18 },
        { name: "Taurine", category: "cardiovascular", reason: "Heart health, blood pressure", priority: "medium", cost: 15 },
        { name: "Citrulline", category: "performance", reason: "Nitric oxide, blood flow", priority: "medium", cost: 20 },
        { name: "Apigenin", category: "sleep", reason: "Sleep quality, anti-inflammatory", priority: "low", cost: 16 }
      ],
      removals: [
        { name: "Multivitamin", reason: "Redundant", savings: 25 },
        { name: "Generic Antioxidant", reason: "Replaced with targeted compounds", savings: 15 },
        { name: "Caffeine Pills", reason: "Use coffee instead", savings: 10 },
        { name: "Random Herbal Blend", reason: "Unproven", savings: 20 },
        { name: "Low-quality Omega-3", reason: "Upgrade to higher EPA/DHA", savings: 0 }
      ],
      modifications: [
        { name: "Glucosamine", change: "→ MSM + Collagen Type II", cost: 0 },
        { name: "Melatonin", change: "→ Lower dose (0.3mg), cyclical use", cost: -5 },
        { name: "Fish Oil", change: "→ Higher EPA/DHA concentration", cost: 15 },
        { name: "Magnesium", change: "→ Split dose (AM/PM)", cost: 0 },
        { name: "Zinc", change: "→ Add Copper to balance", cost: 8 },
        { name: "Vitamin D3", change: "→ Add K2-MK7", cost: 12 }
      ]
    }
  },

  dailyProtocol: {
    morning: {
      time: "6:00 AM - 8:00 AM",
      fasted: [
        { name: "Black Coffee", icon: "☕" },
        { name: "Creatine (5g)", icon: "💪" }
      ],
      withBreakfast: [
        { name: "Omega-3 (2g EPA/DHA)", icon: "🐟" },
        { name: "Vitamin D3 + K2 (5000 IU)", icon: "☀️" },
        { name: "Tongkat Ali (400mg)", icon: "🌿" },
        { name: "Boron (6mg)", icon: "⚡" },
        { name: "Zinc + Copper (25mg/2mg)", icon: "🔬" },
        { name: "Lutein + Zeaxanthin (20mg)", icon: "👁️" },
        { name: "Astaxanthin (12mg)", icon: "🦐" },
        { name: "B-Complex", icon: "🅱️" },
        { name: "Vitamin C (1000mg)", icon: "🍊" }
      ]
    },
    afternoon: {
      time: "12:00 PM - 2:00 PM",
      withLunch: [
        { name: "Magnesium Glycinate (200mg)", icon: "⚡" },
        { name: "Red Yeast Rice (1200mg)", icon: "❤️" },
        { name: "Bergamot (500mg)", icon: "🍋" },
        { name: "CoQ10 (200mg)", icon: "⚡" },
        { name: "Probiotics (50B CFU)", icon: "🦠" }
      ],
      preworkout: [
        { name: "Citrulline (6g)", icon: "💪" },
        { name: "Rhodiola (300mg)", icon: "🌿" },
        { name: "Taurine (2g)", icon: "⚡" }
      ]
    },
    evening: {
      time: "6:00 PM - 8:00 PM",
      withDinner: [
        { name: "Omega-3 (2g EPA/DHA)", icon: "🐟" },
        { name: "NAC (600mg)", icon: "🛡️" },
        { name: "Stinging Nettle Root (500mg)", icon: "🌿" },
        { name: "Ashwagandha (600mg)", icon: "🧘" },
        { name: "Bilberry Extract (160mg)", icon: "👁️" }
      ],
      postWorkout: [
        { name: "Whey Protein (30g)", icon: "🥛" },
        { name: "Collagen Type II (40mg)", icon: "🦴" }
      ]
    },
    night: {
      time: "10:00 PM - 11:00 PM",
      beforeBed: [
        { name: "Magnesium Glycinate (200mg)", icon: "😴" },
        { name: "Apigenin (50mg)", icon: "🌙" },
        { name: "Melatonin (0.3mg, cyclical)", icon: "💤" }
      ]
    }
  },

  bodySystems: {
    brain: {
      supplements: ["Omega-3", "B-Complex", "Rhodiola", "Ashwagandha", "CoQ10"],
      impact: "Cognitive function, focus, stress resilience"
    },
    heart: {
      supplements: ["Omega-3", "Red Yeast Rice", "Bergamot", "CoQ10", "Taurine", "Magnesium"],
      impact: "Cholesterol management, blood pressure, cardiovascular health"
    },
    muscles: {
      supplements: ["Whey Protein", "Creatine", "Citrulline", "Taurine", "Magnesium"],
      impact: "Strength, recovery, performance"
    },
    eyes: {
      supplements: ["Lutein", "Zeaxanthin", "Astaxanthin", "Bilberry", "Omega-3"],
      impact: "Macular protection, night vision, eye fatigue"
    },
    joints: {
      supplements: ["Collagen Type II", "MSM", "Omega-3", "Astaxanthin"],
      impact: "Joint health, flexibility, inflammation"
    },
    liver: {
      supplements: ["NAC", "Milk Thistle", "Vitamin C", "Omega-3"],
      impact: "Detoxification, glutathione production"
    },
    hormones: {
      supplements: ["Tongkat Ali", "Boron", "Stinging Nettle", "Zinc", "Vitamin D", "Magnesium", "Ashwagandha"],
      impact: "Testosterone optimization, SHBG reduction"
    }
  },

  synergies: [
    {
      primary: "Vitamin D3",
      secondary: "K2-MK7",
      strength: "high",
      explanation: "K2 directs calcium to bones, prevents arterial calcification"
    },
    {
      primary: "Zinc",
      secondary: "Copper",
      strength: "high",
      explanation: "Maintain proper zinc:copper ratio to prevent imbalance"
    },
    {
      primary: "Omega-3",
      secondary: "Astaxanthin",
      strength: "high",
      explanation: "Astaxanthin protects omega-3 from oxidation"
    },
    {
      primary: "Tongkat Ali",
      secondary: "Boron",
      strength: "high",
      explanation: "Synergistic testosterone optimization and SHBG reduction"
    },
    {
      primary: "Magnesium",
      secondary: "Vitamin D",
      strength: "medium",
      explanation: "Magnesium required for Vitamin D metabolism"
    },
    {
      primary: "Red Yeast Rice",
      secondary: "CoQ10",
      strength: "high",
      explanation: "Red yeast rice depletes CoQ10, supplementation essential"
    },
    {
      primary: "Citrulline",
      secondary: "Taurine",
      strength: "medium",
      explanation: "Enhanced nitric oxide production and performance"
    },
    {
      primary: "Lutein",
      secondary: "Zeaxanthin",
      strength: "high",
      explanation: "Work together for macular protection"
    },
    {
      primary: "NAC",
      secondary: "Vitamin C",
      strength: "medium",
      explanation: "Enhanced glutathione production and antioxidant capacity"
    },
    {
      primary: "Ashwagandha",
      secondary: "Rhodiola",
      strength: "medium",
      explanation: "Complementary adaptogenic stress response"
    }
  ],

  actionItems: [
    {
      id: 1,
      title: "Start Boron supplementation (6mg daily)",
      category: "supplement",
      priority: "high",
      impact: "high",
      effort: "low",
      estimatedTime: "2 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Boron reduces SHBG by up to 25%, increasing free testosterone"
    },
    {
      id: 2,
      title: "Add Stinging Nettle Root (500mg daily)",
      category: "supplement",
      priority: "high",
      impact: "high",
      effort: "low",
      estimatedTime: "2 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Blocks SHBG binding sites, liberating more free testosterone"
    },
    {
      id: 3,
      title: "Implement Red Yeast Rice + Bergamot for cholesterol",
      category: "supplement",
      priority: "high",
      impact: "high",
      effort: "low",
      estimatedTime: "5 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Natural approach to reduce LDL by 20-30%"
    },
    {
      id: 4,
      title: "Start comprehensive vision stack (Lutein, Astaxanthin, Bilberry)",
      category: "supplement",
      priority: "high",
      impact: "high",
      effort: "low",
      estimatedTime: "5 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Currently score 45/100 in vision - critical for longevity"
    },
    {
      id: 5,
      title: "Remove redundant multivitamin",
      category: "optimization",
      priority: "medium",
      impact: "medium",
      effort: "low",
      estimatedTime: "1 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Targeted supplementation is more effective"
    },
    {
      id: 6,
      title: "Retest blood work in 3 months",
      category: "testing",
      priority: "high",
      impact: "high",
      effort: "medium",
      estimatedTime: "2 hours",
      dueDate: "Month 3",
      status: "pending",
      details: "Monitor SHBG, LDL, Free T, HDL progress"
    },
    {
      id: 7,
      title: "Add K2-MK7 to Vitamin D3",
      category: "supplement",
      priority: "high",
      impact: "high",
      effort: "low",
      estimatedTime: "2 min",
      dueDate: "Week 1",
      status: "pending",
      details: "Essential cofactor for proper calcium metabolism"
    },
    {
      id: 8,
      title: "Split magnesium dose (AM/PM)",
      category: "timing",
      priority: "low",
      impact: "medium",
      effort: "low",
      estimatedTime: "1 min",
      dueDate: "Week 2",
      status: "pending",
      details: "Better absorption and sustained benefits"
    },
    {
      id: 9,
      title: "Upgrade to high-EPA/DHA omega-3",
      category: "supplement",
      priority: "medium",
      impact: "medium",
      effort: "low",
      estimatedTime: "5 min",
      dueDate: "Week 2",
      status: "pending",
      details: "2g combined EPA/DHA for cardiovascular protection"
    },
    {
      id: 10,
      title: "Consult physician about statin alternatives",
      category: "medical",
      priority: "high",
      impact: "high",
      effort: "high",
      estimatedTime: "1 hour",
      dueDate: "Month 1",
      status: "pending",
      details: "Discuss natural cholesterol management vs pharmaceutical intervention"
    }
  ],

  costAnalysis: {
    categories: {
      hormones: { current: 80, optimized: 120, change: 40 },
      cardiovascular: { current: 45, optimized: 110, change: 65 },
      performance: { current: 85, optimized: 95, change: 10 },
      vision: { current: 0, optimized: 72, change: 72 },
      cognitive: { current: 65, optimized: 65, change: 0 },
      recovery: { current: 50, optimized: 55, change: 5 },
      immune: { current: 35, optimized: 35, change: 0 },
      general: { current: 90, optimized: 0, change: -90 }
    },
    healthGoals: {
      "Optimize Testosterone": 153,
      "Improve Cholesterol": 110,
      "Vision Protection": 72,
      "Performance & Recovery": 150,
      "Cognitive Enhancement": 65,
      "General Health": 35
    },
    roi: [
      {
        goal: "Testosterone Optimization",
        cost: 153,
        benefit: "15-25% increase in free T",
        healthImpact: 95
      },
      {
        goal: "Cholesterol Management",
        cost: 110,
        benefit: "20-30% LDL reduction",
        healthImpact: 90
      },
      {
        goal: "Vision Protection",
        cost: 72,
        benefit: "50% reduction in macular degeneration risk",
        healthImpact: 85
      }
    ]
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = healthData;
}
