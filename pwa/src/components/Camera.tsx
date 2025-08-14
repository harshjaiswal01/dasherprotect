/**
 * Camera preview using getUserMedia. In M2 we’ll add face crop + ONNX embedding.
 */
import React, { useEffect, useRef } from 'react';

export default function Camera() {
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        let stream: MediaStream;
        (async () => {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" }, audio: false });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                await videoRef.current.play();
            }
        })();
        return () => { stream && stream.getTracks().forEach(t => t.stop()); }
    }, []);

    return (
        <div className="w-full">
            <video ref={videoRef} className="w-full rounded-md" playsInline muted />
        </div>
    );
}
