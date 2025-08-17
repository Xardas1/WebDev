import React from 'react';
import { Link } from 'react-router-dom';
import { FiZap, FiBell, FiCheckCircle } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import { CircleCheck } from 'lucide-react';
import { Clover } from 'lucide-react';
import { Rocket } from 'lucide-react';
import { ChevronRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  // Smart navigation function
  const handleTryItFree = () => {
    console.log("🔄 Try it free clicked!");
    console.log("📊 Auth state:", { user, loading });
    
    if (loading) {
      console.log("⏳ Still loading, waiting...");
      return; // Don't navigate while loading
    }
    
    if (user) {
      console.log("✅ User is logged in, going to product page");
      // User is logged in, go to product page
      window.location.href = "https://app.re-mind.xyz/product";
    } else {
      console.log("❌ User is NOT logged in, going to login page");
      // User is not logged in, go to login page
      window.location.href = "https://app.re-mind.xyz/login";
    }
  };

  // bg-gradient-to-br from-[#fdfcf9] to-[#f6f3ef] option 1
  // bg-gradient-to-br from-[#f5f7fa] to-[#e4e7eb]
  return (

      <div className="flex flex-col min-h-screen bg-gradient-to-br from-[#f5f7fa] to-[#e4e7eb]">
        <main className="flex-grow flex justify-center">
              <div className="mt-6 mb-12 px-4 md:px-12">
                <div className="text-black flex flex-col justify-center">


                <div className="text-center flex flex-col items-center">
                    <h1 className="font-['Poppins'] font-extrabold text-4xl sm:text-5xl md:text-6xl lg:text-7xl tracking-tight leading-tight mb-3">
                      Never Forget &<br /> Waste Your <br />
                      Money Ever Again
                    </h1>


                    <p className="font-['Inter'] text-lg text-gray-600 leading-relaxed max-w-md md:max-w-xl mb-8 mb-6">
                      Re:Mind brings you a slek, modern way to always remember about 
                      your subscriptions and never waste money again. With just few clicks you can stop 
                      wasting and enjoy your full pocket again.</p>
                
                {/* Debug info - remove this later */}
                <div className="mb-4 p-3 bg-gray-100 rounded-lg text-sm">
                  <p><strong>Debug Info:</strong></p>
                  <p>Loading: {loading ? "Yes" : "No"}</p>
                  <p>User: {user ? `Logged in as ${user.username}` : "Not logged in"}</p>
                  <p>Current domain: {window.location.hostname}</p>
                  <p>All cookies: {document.cookie || "No cookies found"}</p>
                  <button 
                    onClick={() => {
                      console.log("🧪 Test button clicked");
                      console.log("🔍 Current cookies:", document.cookie);
                      console.log("🔍 User state:", user);
                      console.log("🔍 Loading state:", loading);
                      console.log("🔍 Current domain:", window.location.hostname);
                      
                      // Test if we can access cookies from different domains
                      console.log("🔍 Cookies for .re-mind.xyz:", document.cookie.split(';').filter(c => c.includes('token')));
                      console.log("🔍 Cookies for current domain:", document.cookie.split(';').filter(c => c.includes('token')));
                    }}
                    className="mt-2 px-3 py-1 bg-blue-500 text-white rounded text-xs"
                  >
                    Test Auth Status
                  </button>
                </div>

                  <div className="">
                    <button
                      onClick={handleTryItFree}
                      className="bg-black text-white px-8 py-3 mb-5 rounded-lg hover:bg-neutral-800 active:scale-95 transition-transform shadow-md font-semibold tracking-wide text-base cursor-pointer"
                    >
                      Try it free
                    </button>
                  </div>
                  </div>

                <div className="flex justify-center mt-12">
                  <h1 className="text-5xl font-['Poppins']" > Everything You Need to Stop Wasting Money Now</h1>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 m-6">
                  <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
                    <div className="text-purple-600 text-3xl mb-4">🔔</div>
                    <h3 className="text-lg font-semibold mb-2">Stop forgetting subscriptions</h3>
                    <p className="text-gray-600 font-['Inter']">Never forget a subscription again. Stop wasting money on services you don't use.</p>
                  </div>

                <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
                  <div className="text-purple-600 text-3xl mb-4">💸</div> 
                  <h3 className="text-lg font-semibold mb-2">Safe money monthly</h3>
                  <p className="text-gray-600 font-['Inter']">Save money every month — up to $5,000 over your lifetime. Don't pay for what you don't need.</p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
                  <div className="text-purple-600 text-3xl mb-4">⚡</div> 
                  <h3 className="text-lg font-semibold mb-2">Quick Setup</h3>
                  <p className="text-gray-600 font-['Inter']">Get started in under two minutes with a simple, streamlined setup.</p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
                  <div className="text-purple-600 text-3xl mb-4">🔐</div> 
                  <h3 className="text-lg font-semibold mb-2">No sensitive data required</h3>
                  <p className="text-gray-600 font-['Inter']">No sensitive data needed — just sign up and start using it instantly.</p>
                </div>

                </div>

                <div className="text-center text-4xl font-['Poppins']"> 
                  <h1>How it works?</h1>
                </div>

              <div className="text-center mb-6 mt-6">
                  <button
                    onClick={handleTryItFree}
                    className="bg-black text-white px-8 py-3 rounded-lg hover:bg-neutral-800 transition shadow-md fong-semibold tracking-wide text-base cursor-pointer"
                  >
                    Try It Free
                  </button>
              </div>


                <p className="text-lg text-text/80 max-w-2xl mx-auto text-gray-700 mt-1 mb-6"> Three simple steps. One confident learner.</p>


                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  <div className="relative bg-white p-6 rounded-3xl shadow-md hover:shadow-lg transition">
                    
                  <div className="w-12 h-12 bg-blue-100 flex items-center justify-center rounded-full mb-5">
                    <CircleCheck className="w-10 h-10 text-blue-500"></CircleCheck>
                  </div>

                  <div className="absolute top-27 right-1 text-gray-300">
                    <ChevronRight className="w-10 h-10" />
                  </div>

                    <p className="text-sm text-blue-500 font-bold tracking-wide uppercase mb-1">
                      Step 1
                    </p>
                    <h3 className="text-[18px] font-bold mb-2">
                      Sign Up On Our Page  
                    </h3>
                    <p className="text-gray-600 font-['Inter'] leading-relaxed">
                      Sign up in seconds. Just a few clicks and you're all set
                    </p>            
                  </div>

                  <div className="relative bg-white p-6 rounded-3xl shadow-md hover:shadow-lg transition">
                  <div className="w-12 h-12 bg-green-100 flex items-center justify-center rounded-full mb-5">
                    <Clover className="w-10 h-10 text-green-500" />
                  </div>

                  <div className="absolute top-27 right-1 text-gray-300">
                    <ChevronRight className="w-10 h-10" />
                  </div>

                    <p className="text-sm text-green-500 font-bold tracking-wide uppercase mb-1">
                      Step 2
                    </p>
                    <h3 className="text-[18px] font-bold mb-2">
                      Choose a Subscription
                    </h3>
                    <p className="text-gray-600 font-['Inter'] leading-relaxed">
                      Add any subscription, set a name and reminder — done in seconds
                    </p>
                  </div>


                  <div className="bg-white p-6 rounded-3xl shadow-md hover:shadow-lg transition">
                  <div className="w-12 h-12 bg-amber-100 flex items-center justify-center rounded-full mb-5">
                    <Rocket className="w-10 h-10 text-amber-500"></Rocket>
                  </div>
                    <p className="text-sm text-amber-500 font-bold tracking-wide uppercase mb-1">
                      Step 3
                    </p>
                    <h3 className="text-[18px] font-bold mb-2">
                      Just Wait
                    </h3>
                    <p className="text-gray-600 font-['Inter']">
                      A reminder lands in your inbox days before your next payment
                    </p>
                  </div>
                </div>

                <div className="flex justify-center text-white "> 
                <div className="w-full max-w-[1000px] px-4 md:px-10 bg-gradient-to-r from-gray-900 to-gray-800 pt-8 pb-10 px-10 rounded-3xl shadow-md hover:shadow-lg transition text-center mt-10 mb-6 ">
                  <h1 className="text-3xl font-['Poppins] mt-5"> Sign Up Now And Never Waste Your Money Again</h1>
                  <p className="mt-4 text-xl mb-8 "> Stop wasting money on things you don't use, click here to try it for free no hidden costs</p>

                  <button
                    onClick={handleTryItFree}
                    className="bg-black text-white px-8 py-3 rounded-lg hover:bg-neutral-800 transition shadow-md fong-semibold tracking-wide text-base mt-7 cursor-pointer"
                  >
                    Try It Free
                  </button>

                  </div>
              </div>    
           </div>
          </div>
      </main>
    <footer className="bg-black w-full py-4">
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center text-sm text-white">
        <a href="/privacy" className="hover:underline">Privacy Policy</a>
        <p className="text-gray-400">© 2025 Re:Mind. All rights reserved.</p>
      </div>
    </footer>
  </div>

  );
};

export default Home;


