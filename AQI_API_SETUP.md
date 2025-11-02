# Air Quality Index (AQI) API Setup

This application uses the **World Air Quality Index (WAQI)** API to fetch real-time air quality data.

## Getting Your Free API Key

### Option 1: WAQI API (Recommended - Free)

1. Visit [https://aqicn.org/data-platform/token/](https://aqicn.org/data-platform/token/)
2. Fill out the form with:
   - Your name
   - Your email address
   - A brief description of your project (e.g., "Health monitoring app for personal use")
3. Submit the form
4. You'll receive your API token via email within a few minutes
5. Add the token to your `.env.local` file:
   ```
   NEXT_PUBLIC_WAQI_API_KEY=your_api_token_here
   ```

### Option 2: OpenWeatherMap Air Pollution API (Alternative)

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key
5. You would need to modify the code to use OpenWeatherMap instead of WAQI

## API Features

### WAQI API Provides:
- Real-time AQI (Air Quality Index)
- PM2.5, PM10 levels
- Ozone (O₃) levels
- Nitrogen Dioxide (NO₂) levels
- Sulfur Dioxide (SO₂) levels
- Carbon Monoxide (CO) levels
- Global coverage (most cities worldwide)
- Free tier: 1000 requests per day

## Setup Instructions

1. **Create `.env.local` file** (if it doesn't exist):
   ```bash
   # In the root directory of the project
   touch .env.local
   ```

2. **Add your API key**:
   ```
   NEXT_PUBLIC_WAQI_API_KEY=your_actual_api_key_here
   ```

3. **Restart your development server**:
   ```bash
   npm run dev
   # or
   pnpm dev
   # or
   yarn dev
   ```

4. **Verify it's working**:
   - Navigate to the Air Quality page in your dashboard
   - You should see a "Live Data" badge next to the location
   - The data should reflect real-time AQI for your selected location

## Troubleshooting

### "Demo Data" badge is showing
- Check that your `.env.local` file exists in the root directory
- Verify the API key is correctly formatted (no extra spaces)
- Restart your development server after adding the key
- Check the browser console for any error messages

### API request failing
- Verify your internet connection
- Check that you haven't exceeded the free tier limit (1000 requests/day)
- Ensure the API key is valid and active
- Try accessing the API directly in your browser:
  ```
  https://api.waqi.info/feed/delhi/?token=YOUR_API_KEY
  ```

### Location not found
- Try using different location formats:
  - City name: `Delhi`
  - City, Country: `Delhi, India`
  - Coordinates: `@28.6139,77.2090`
  - Station ID: `@8877`

## Supported Locations

The WAQI API supports over 12,000 stations in 1000+ major cities worldwide, including:

**India**: Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad
**USA**: New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia
**China**: Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu
**Europe**: London, Paris, Berlin, Madrid, Rome, Amsterdam
**Others**: Tokyo, Seoul, Bangkok, Singapore, Hong Kong, Dubai

## Demo Data Fallback

If the API key is not configured or the API request fails, the application will automatically fall back to demo data to ensure the app remains functional.

## API Documentation

For more details about the WAQI API:
- Documentation: [https://aqicn.org/json-api/doc/](https://aqicn.org/json-api/doc/)
- Support: [https://aqicn.org/contact/](https://aqicn.org/contact/)

## Privacy & Security

- The API key is prefixed with `NEXT_PUBLIC_` which means it's exposed to the client
- This is acceptable for WAQI as it's designed for client-side use
- The free tier has rate limits that prevent abuse
- Never commit your `.env.local` file to version control (it's already in `.gitignore`)
