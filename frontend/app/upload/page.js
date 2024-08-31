"use client"

import React, { useState } from 'react';
import Sidebar from '../components/layout/      Sidebar';
import Topbar from '../components/layout/      Topbar';
import Loader from '../components/loader/Loader';
import { uploadFiles } from '../api/api';
import { motion, AnimatePresence } from 'framer-motion';

const UploadPage = () => {
  const [files, setFiles] = useState({ payment: null, mtr: null });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFiles({ ...files, [e.target.name]: e.target.files[0] });
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('payment_file', files.payment);
    formData.append('mtr_file', files.mtr);

    setLoading(true);
    try {
      const response = await uploadFiles(formData);
      console.log('Upload response:', response);
      setMessage(response.message);
    } catch (error) {
      console.error('Upload failed:', error);
      setMessage('Failed to upload files. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <div className="p-4">
          <div className="mb-4">
            <label className="block">Payment Report</label>
            <input type="file" name="payment" onChange={handleFileChange} />
          </div>
          <div className="mb-4">
            <label className="block">Merchant Tax Report (MTR)</label>
            <input type="file" name="mtr" onChange={handleFileChange} />
          </div>
          <button
            onClick={handleUpload}
            className="bg-purple-700 text-white px-4 py-2 rounded-md"
            disabled={loading} 
          >
            {loading ? 'Uploading...' : 'Upload'}
          </button>

          <AnimatePresence>
            {loading && <Loader />}
          </AnimatePresence>

          <AnimatePresence>
            {!loading && message && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
                className={`mt-4 p-4 rounded-md ${message.includes('Successfully') ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}
              >
                {message}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
