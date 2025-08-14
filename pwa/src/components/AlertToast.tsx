/**
 * Simple toast placeholder; in M3 we’ll wire to `hit_detected`.
 */
import React from 'react';
export default function AlertToast({ text }: { text: string }) {
    return <div className="fixed bottom-4 right-4 border bg-white p-3 shadow">{text}</div>;
}
