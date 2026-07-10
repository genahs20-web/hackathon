/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0F1117",
        surface: "#1A1D27",
        card: "#21253A",
        border: "#2E3350",
        primary: "#6366F1",
        secondary: "#94A3B8",
        accent: "#818CF8",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",
        muted: "#64748B",
      },
      backgroundImage: {
        "gradient-brand": "linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)",
      },
    },
  },
  plugins: [],
};

