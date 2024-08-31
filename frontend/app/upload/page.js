// app/upload/page.js
"use client"

import React, { useState } from 'react';
import Sidebar from '../components/layout/      Sidebar';
import Topbar from '../components/layout/      Topbar';
import { uploadFiles } from '../api/api';

const UploadPage = () => {
  const [files, setFiles] = useState({ payment: null, mtr: null });

  const handleFileChange = (e) => {
    setFiles({ ...files, [e.target.name]: e.target.files[0] });
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('payment', files.payment);
    formData.append('mtr', files.mtr);

    const response = await uploadFiles(formData);
    console.log('Upload response:', response);
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
          <button onClick={handleUpload} className="bg-purple-700 text-white px-4 py-2 rounded-md">
            Upload
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
