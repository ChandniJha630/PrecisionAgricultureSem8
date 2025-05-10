module.exports = {
    // Specify the paths to all of your template files
    content: [
      "./src/**/*.{html,js,jsx,ts,tsx}", // Tailwind will scan these files for class names
    ],
    theme: {
      extend: {
        // You can extend the default Tailwind theme here if needed
      },
    },
    plugins: [
      // You can add Tailwind plugins here if required (e.g., forms, typography, etc.)
    ],
  }
  