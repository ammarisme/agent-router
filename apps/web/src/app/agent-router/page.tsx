'use client'

import React, { useEffect, useMemo, useRef, useState } from "react";
import { useApi } from "@/providers/ApiProvider";
import type { Agent, Feature, Route, Role } from "@/lib/api";

// ---------- Types ----------
interface Connection {
  agentId: string;
  featureId: string;
  agentName: string;
  featureName: string;
  style: string;
  rules: {
    allowAll: boolean;
    allowed: string[];
    disallowed: string[];
  };
  conditional?: boolean;
}

interface Connection {
  agentId: string;
  featureId: string;
  agentName: string;
  featureName: string;
  style: string;
  rules: {
    allowAll: boolean;
    allowed: string[];
    disallowed: string[];
  };
  conditional?: boolean;
}

interface Point {
  x: number;
  y: number;
}

// ---------- Constants ----------
const ROLE_OPTIONS = [
  "Program Author",
  "Learner",
  "Reviewer",
  "Admin",
  "Manager",
  "Guest",
];

// ---------- Utilities ----------
function uid() {
  return (
    Date.now().toString(36) + Math.random().toString(36).slice(2, 8)
  ).toUpperCase();
}

function centerY(el: HTMLElement | null): number {
  if (!el) return 0;
  const r = el.getBoundingClientRect();
  return r.top + r.height / 2;
}

function rect(el: HTMLElement | null): DOMRect {
  if (!el) return { left: 0, top: 0, right: 0, bottom: 0, width: 0, height: 0 } as DOMRect;
  const r = el.getBoundingClientRect();
  return r;
}

function useResizeObserver(targetRef: React.RefObject<HTMLElement>, cb: () => void) {
  useEffect(() => {
    const el = targetRef.current;
    if (!el) return;
    const obs = new ResizeObserver(() => cb());
    obs.observe(el);
    window.addEventListener("resize", cb, { passive: true });
    return () => {
      obs.disconnect();
      window.removeEventListener("resize", cb);
    };
  }, [targetRef, cb]);
}

// Cubic bezier path from A to B using horizontal control points for nice S-curves
function bezierPath(a: Point, b: Point): string {
  const dx = Math.max(60, Math.abs(b.x - a.x) * 0.35);
  return `M ${a.x} ${a.y} C ${a.x + dx} ${a.y}, ${b.x - dx} ${b.y}, ${b.x} ${b.y}`;
}

function bezierPointHalf(a: Point, b: Point): Point {
  const dx = Math.max(60, Math.abs(b.x - a.x) * 0.35);
  const c1 = { x: a.x + dx, y: a.y };
  const c2 = { x: b.x - dx, y: b.y };
  const t = 0.5;
  const mt = 1 - t;
  const x =
    mt * mt * mt * a.x +
    3 * mt * mt * t * c1.x +
    3 * mt * t * t * c2.x +
    t * t * t * b.x;
  const y =
    mt * mt * mt * a.y +
    3 * mt * mt * t * c1.y +
    3 * mt * t * t * c2.y +
    t * t * t * b.y;
  return { x, y };
}

// ---------- UI Primitives ----------
function LaneHeader({ title, count, right }: { title: string; count: number; right: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-3 mb-3">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
        <span className="text-xs text-zinc-400">{count}</span>
      </div>
      <div className="flex items-center gap-2">{right}</div>
    </div>
  );
}

function Pill({ children, active, activeColor = "indigo", onMouseDown, onMouseUp, onClick }: { 
  children: React.ReactNode; 
  active?: boolean; 
  activeColor?: "indigo" | "green";
  onMouseDown?: () => void; 
  onMouseUp?: () => void; 
  onClick?: () => void; 
}) {
  const ringColor = activeColor === "green" ? "ring-green-500" : "ring-indigo-500";
  
  return (
    <div
      onMouseDown={onMouseDown}
      onMouseUp={onMouseUp}
      onClick={onClick}
      className={
        "px-3 py-2 w-full text-left rounded-xl border transition select-none cursor-pointer " +
        (active
          ? `bg-zinc-800 border-zinc-600 ring-2 ${ringColor}`
          : "bg-zinc-900 border-zinc-800 hover:border-zinc-700 hover:bg-zinc-800")
      }
    >
      {children}
    </div>
  );
}

function Modal({ open, title, children, onClose, footer }: { 
  open: boolean; 
  title: string; 
  children: React.ReactNode; 
  onClose: () => void; 
  footer?: React.ReactNode; 
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative w-full max-w-3xl rounded-2xl border border-zinc-700 bg-zinc-900 p-5 shadow-xl">
        <div className="flex items-start justify-between mb-3">
          <h3 className="text-lg font-semibold">{title}</h3>
          <button
            className="px-2 py-1 text-sm rounded-md border border-zinc-700 hover:bg-zinc-800"
            onClick={onClose}
          >
            Close
          </button>
        </div>
        {children}
        {footer && <div className="mt-4">{footer}</div>}
      </div>
    </div>
  );
}

function RoleSelector({ valueAll, valueAllowed, valueDisallowed, onChange }: { 
  valueAll: boolean; 
  valueAllowed: string[]; 
  valueDisallowed: string[]; 
  onChange: (rules: { allowAll: boolean; allowed: string[]; disallowed: string[] }) => void; 
}) {
  const [allowAll, setAllowAll] = useState(valueAll);
  const [allowed, setAllowed] = useState(new Set(valueAllowed || []));
  const [disallowed, setDisallowed] = useState(new Set(valueDisallowed || []));

  useEffect(() => setAllowAll(valueAll), [valueAll]);
  useEffect(() => setAllowed(new Set(valueAllowed || [])), [valueAllowed]);
  useEffect(() => setDisallowed(new Set(valueDisallowed || [])), [valueDisallowed]);

  function toggle(setter: React.Dispatch<React.SetStateAction<Set<string>>>, set: Set<string>, role: string) {
    const next = new Set(set);
    if (next.has(role)) next.delete(role);
    else next.add(role);
    setter(next);
    // Call onChange with the updated values
    const updatedAllowed = setter === setAllowed ? next : allowed;
    const updatedDisallowed = setter === setDisallowed ? next : disallowed;
    onChange({ 
      allowAll, 
      allowed: Array.from(updatedAllowed), 
      disallowed: Array.from(updatedDisallowed) 
    });
  }

  function handleAllowAllChange(checked: boolean) {
    setAllowAll(checked);
    onChange({ 
      allowAll: checked, 
      allowed: Array.from(allowed), 
      disallowed: Array.from(disallowed) 
    });
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="inline-flex items-center gap-2">
          <input
            type="checkbox"
            checked={allowAll}
            onChange={(e) => handleAllowAllChange(e.target.checked)}
          />
          <span className="text-sm">Allow all roles</span>
        </label>
      </div>

      <div className={allowAll ? "opacity-40 pointer-events-none" : ""}>
        <div className="text-sm font-medium mb-2">Allowed roles (when not all)</div>
        <div className="grid grid-cols-2 gap-2">
          {ROLE_OPTIONS.map((r) => (
            <label key={`allow-${r}`} className="inline-flex items-center gap-2">
              <input
                type="checkbox"
                checked={allowed.has(r)}
                onChange={() => toggle(setAllowed, allowed, r)}
              />
              <span className="text-sm">{r}</span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <div className="text-sm font-medium mb-2">Disallowed roles</div>
        <div className="grid grid-cols-2 gap-2">
          {ROLE_OPTIONS.map((r) => (
            <label key={`deny-${r}`} className="inline-flex items-center gap-2">
              <input
                type="checkbox"
                checked={disallowed.has(r)}
                onChange={() => toggle(setDisallowed, disallowed, r)}
              />
              <span className="text-sm">{r}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}

// New: Agent Sources modal (MCP / A2A / Workflow)
function AgentSourcesModal({ open, onClose, onSave }: { 
  open: boolean; 
  onClose: () => void; 
  onSave: (payload: { type: string; name: string; endpoint: string; apiKey: string }) => void; 
}) {
  const [type, setType] = useState("MCP Server");
  const [name, setName] = useState("");
  const [endpoint, setEndpoint] = useState("");
  const [apiKey, setApiKey] = useState("");

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Connect Agent Source"
      footer={(
        <div className="flex items-center justify-end gap-2 pt-2">
          <button className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800" onClick={onClose}>Cancel</button>
          <button
            className="px-3 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500"
            onClick={() => onSave({ type, name, endpoint, apiKey })}
            disabled={!name || !endpoint}
          >
            Connect
          </button>
        </div>
      )}
    >
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <label className="text-sm">Type
            <select className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={type} onChange={(e)=>setType(e.target.value)}>
              <option>MCP Server</option>
              <option>A2A Registry</option>
              <option>Workflow Engine</option>
            </select>
          </label>
          <label className="text-sm">Name
            <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={name} onChange={(e)=>setName(e.target.value)} placeholder="e.g., Orchestrator Alpha" />
          </label>
        </div>
        <label className="text-sm">Endpoint URL
          <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={endpoint} onChange={(e)=>setEndpoint(e.target.value)} placeholder="https://..." />
        </label>
        <label className="text-sm">API Key (optional)
          <input type="password" className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={apiKey} onChange={(e)=>setApiKey(e.target.value)} placeholder="••••••" />
        </label>
        <p className="text-xs text-zinc-500">On connect, agents from this source would load here. (Not implemented in this demo.)</p>
      </div>
    </Modal>
  );
}

// New: Feature Store modal
function FeatureStoreModal({ open, onClose, onSave }: { 
  open: boolean; 
  onClose: () => void; 
  onSave: (payload: { provider: string; name: string; url: string; token: string }) => void; 
}) {
  const [provider, setProvider] = useState("HTTP JSON");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [token, setToken] = useState("");

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add Feature Configuration Store"
      footer={(
        <div className="flex items-center justify-end gap-2 pt-2">
          <button className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800" onClick={onClose}>Cancel</button>
          <button
            className="px-3 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500"
            onClick={() => onSave({ provider, name, url, token })}
            disabled={!name || !url}
          >
            Connect
          </button>
        </div>
      )}
    >
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <label className="text-sm">Provider
            <select className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={provider} onChange={(e)=>setProvider(e.target.value)}>
              <option>HTTP JSON</option>
              <option>Git (raw)</option>
              <option>Amazon S3</option>
              <option>Google Cloud Storage</option>
            </select>
          </label>
          <label className="text-sm">Name
            <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={name} onChange={(e)=>setName(e.target.value)} placeholder="e.g., Features v1" />
          </label>
        </div>
        <label className="text-sm">URL / Bucket path
          <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={url} onChange={(e)=>setUrl(e.target.value)} placeholder="https://... or s3://bucket/key" />
        </label>
        <label className="text-sm">Access token (optional)
          <input type="password" className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={token} onChange={(e)=>setToken(e.target.value)} placeholder="••••••" />
        </label>
        <p className="text-xs text-zinc-500">On connect, features from this store would populate here. (Not implemented in this demo.)</p>
      </div>
    </Modal>
  );
}

// New: IAM Roles Import modal
function IAMRolesImportModal({ open, onClose }: { 
  open: boolean; 
  onClose: () => void; 
}) {
  const [provider, setProvider] = useState("AWS");
  const [accessKey, setAccessKey] = useState("");
  const [secretKey, setSecretKey] = useState("");
  const [region, setRegion] = useState("us-east-1");
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);

  // Mock IAM roles data
  const mockIAMRoles = [
    "arn:aws:iam::123456789012:role/EC2FullAccess",
    "arn:aws:iam::123456789012:role/S3ReadOnlyAccess",
    "arn:aws:iam::123456789012:role/LambdaExecutionRole",
    "arn:aws:iam::123456789012:role/CloudWatchLogsRole",
    "arn:aws:iam::123456789012:role/CodeDeployServiceRole",
  ];

  const handleImport = () => {
    // Mock import functionality
    console.log("Importing IAM roles:", selectedRoles);
    onClose();
  };

  const toggleRole = (role: string) => {
    setSelectedRoles(prev => 
      prev.includes(role) 
        ? prev.filter(r => r !== role)
        : [...prev, role]
    );
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Import IAM Roles"
      footer={(
        <div className="flex items-center justify-end gap-2 pt-2">
          <button className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800" onClick={onClose}>Cancel</button>
          <button
            className="px-3 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500"
            onClick={handleImport}
            disabled={selectedRoles.length === 0}
          >
            Import {selectedRoles.length} Role{selectedRoles.length !== 1 ? 's' : ''}
          </button>
        </div>
      )}
    >
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <label className="text-sm">Cloud Provider
            <select className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={provider} onChange={(e)=>setProvider(e.target.value)}>
              <option>AWS</option>
              <option>Azure</option>
              <option>Google Cloud</option>
            </select>
          </label>
          <label className="text-sm">Region
            <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={region} onChange={(e)=>setRegion(e.target.value)} placeholder="us-east-1" />
          </label>
        </div>
        
        <div className="space-y-2">
          <label className="text-sm">Access Key ID
            <input className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={accessKey} onChange={(e)=>setAccessKey(e.target.value)} placeholder="AKIA..." />
          </label>
          <label className="text-sm">Secret Access Key
            <input type="password" className="mt-1 w-full rounded-md bg-zinc-900 border border-zinc-700 p-2 text-sm" value={secretKey} onChange={(e)=>setSecretKey(e.target.value)} placeholder="••••••" />
          </label>
        </div>

        <div className="border-t border-zinc-700 pt-4">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-medium">Available IAM Roles</h4>
            <span className="text-xs text-zinc-400">{selectedRoles.length} selected</span>
          </div>
          <div className="max-h-48 overflow-y-auto space-y-2">
            {mockIAMRoles.map((role) => (
              <label key={role} className="flex items-center gap-2 p-2 rounded-md hover:bg-zinc-800/50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedRoles.includes(role)}
                  onChange={() => toggleRole(role)}
                  className="rounded"
                />
                <span className="text-sm text-zinc-300">{role}</span>
              </label>
            ))}
          </div>
        </div>

        <p className="text-xs text-zinc-500">
          Imported IAM roles will be available as role options in your agent routing configurations.
        </p>
      </div>
    </Modal>
  );
}

// ---------- Routes Table ----------
function summarizeRules(r: { allowAll: boolean; allowed: string[]; disallowed: string[] } | undefined) {
  if (!r) return "—";
  if (r.allowAll) return "All roles";
  const allow = r.allowed?.length || 0;
  const deny = r.disallowed?.length || 0;
  const parts = [];
  if (allow) parts.push(`Allow: ${allow}`);
  if (deny) parts.push(`Block: ${deny}`);
  return parts.length ? parts.join(" • ") : "Custom";
}

function RoutesTable({ routes, onEdit, onRemove }: { 
  routes: Connection[]; 
  onEdit: (conn: Connection) => void; 
  onRemove: (conn: Connection) => void; 
}) {
  return (
    <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/40 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold">Routes</h3>
        <span className="text-xs text-zinc-400">{routes.length}</span>
      </div>
      {routes.length === 0 ? (
        <div className="text-sm text-zinc-400">No routes yet. Create one by dragging a Feature onto an Agent, or use Add conditional route.</div>
      ) : (
        <div className="overflow-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-zinc-400">
                <th className="text-left font-medium py-2 pr-4">Feature</th>
                <th className="text-left font-medium py-2 pr-4">Agent</th>
                <th className="text-left font-medium py-2 pr-4">Roles</th>
                <th className="text-left font-medium py-2 pr-4">Conditional</th>
                <th className="text-right font-medium py-2 pl-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {routes.map((c: Connection) => (
                <tr key={`${c.agentId}-${c.featureId}`} className="border-t border-zinc-800 hover:bg-zinc-800/40">
                  <td className="py-2 pr-4">{c.featureName}</td>
                  <td className="py-2 pr-4">{c.agentName}</td>
                  <td className="py-2 pr-4">{summarizeRules(c.rules)}</td>
                  <td className="py-2 pr-4">{c.conditional ? <span className="inline-flex items-center rounded-full border border-amber-500/60 px-2 py-0.5 text-amber-300 text-xs">conditional</span> : <span className="text-zinc-400">—</span>}</td>
                  <td className="py-2 pl-4 text-right space-x-2">
                    <button className="px-2 py-1 rounded-md border border-zinc-700 hover:bg-zinc-800" onClick={() => onEdit(c)}>Edit</button>
                    <button className="px-2 py-1 rounded-md border border-zinc-700 hover:bg-zinc-800" onClick={() => onRemove(c)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

// ---------- Main Component ----------
export default function AgentRoutingTool() {
  const { agents, features, loading, error, fetchAgents, fetchFeatures, createAgent, createFeature, importIAMRoles } = useApi();

  const initialConnectionRef = useRef(true);
  const [connections, setConnections] = useState<Connection[]>([]);

  // Edit modal (existing per-route rules)
  const [editing, setEditing] = useState<{ agentId: string; featureId: string } | null>(null); // { agentId, featureId }
  const [draftRules, setDraftRules] = useState<{ allowAll: boolean; allowed: string[]; disallowed: string[] }>({ allowAll: true, allowed: [], disallowed: [] });

  // Conditional route flow state
  const [selectedFeatureId, setSelectedFeatureId] = useState<string | null>(null);
  const [condModalOpen, setCondModalOpen] = useState(false);
  const [condMode, setCondMode] = useState("idle"); // idle | roles | pick-agents | ready
  const [condRules, setCondRules] = useState<{ allowAll: boolean; allowed: string[]; disallowed: string[] }>({ allowAll: true, allowed: [], disallowed: [] });
  const [condDraft, setCondDraft] = useState<{ featureId: string | null; agentIds: string[] }>({ featureId: null, agentIds: [] });

  // NEW: source modals visibility
  const [showAgentSources, setShowAgentSources] = useState(false);
  const [showFeatureStore, setShowFeatureStore] = useState(false);
  const [showIAMRolesImport, setShowIAMRolesImport] = useState(false);
  const [flash, setFlash] = useState<string | null>(null);

  // Load data on component mount
  useEffect(() => {
    fetchAgents();
    fetchFeatures();
  }, [fetchAgents, fetchFeatures]);

  // Create initial connection when data is loaded
  useEffect(() => {
    if (initialConnectionRef.current && agents?.length > 0 && features?.length > 1) {
      initialConnectionRef.current = false;
      setConnections([
        {
          agentId: agents[0].id,
          featureId: features[1].id,
          agentName: agents[0].name,
          featureName: features[1].name,
          style: "dotted",
          rules: { allowAll: true, allowed: [], disallowed: [] },
        },
      ]);
    }
  }, [agents, features]);

  const [draggingFeatureId, setDraggingFeatureId] = useState<string | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);
  const lanesRef = useRef<HTMLDivElement>(null);
  const agentRefs = useRef<Map<string, HTMLElement>>(new Map());
  const featureRefs = useRef<Map<string, HTMLElement>>(new Map());

  const forceRerender = useState(0)[1];
  useResizeObserver(lanesRef, () => forceRerender((x) => x + 1));

  useEffect(() => {
    const fn = () => forceRerender((x) => x + 1);
    window.addEventListener("scroll", fn, true);
    return () => window.removeEventListener("scroll", fn, true);
  }, []);

  // Drag from Feature → drop on Agent (basic route)
  function handleAgentDrop(a: Agent) {
    if (!draggingFeatureId) return;
    const f = features?.find((x) => x.id === draggingFeatureId);
    if (!f) return;

    setConnections((prev) => {
      const exists = prev.some((c) => c.agentId === a.id && c.featureId === f.id);
      if (exists) return prev;
      return [
        ...prev,
        {
          agentId: a.id,
          featureId: f.id,
          agentName: a.name,
          featureName: f.name,
          style: "dotted",
          rules: { allowAll: true, allowed: [], disallowed: [] },
        },
      ];
    });
    setDraggingFeatureId(null);
  }

  function removeConnection(conn: Connection) {
    setConnections((prev) => prev.filter(
      (c) => !(c.agentId === conn.agentId && c.featureId === conn.featureId)
    ));
  }

  const svgBox = useMemo(() => {
    const r = lanesRef.current?.getBoundingClientRect();
    if (!r) return { left: 0, top: 0, width: 0, height: 0 };
    return { left: r.left, top: r.top, width: r.width, height: r.height };
  }, [lanesRef.current, agents?.length || 0, features?.length || 0]);

  // Anchors: Feature right center → Agent left center (requested)
  function featureAnchorRight(id: string): Point {
    const el = featureRefs.current.get(id);
    if (!el) return { x: 0, y: 0 };
    const r = rect(el);
    return { x: r.right - svgBox.left, y: centerY(el) - svgBox.top };
  }
  function agentAnchorLeft(id: string): Point {
    const el = agentRefs.current.get(id);
    if (!el) return { x: 0, y: 0 };
    const r = rect(el);
    return { x: r.left - svgBox.left, y: centerY(el) - svgBox.top };
  }

  function openEdit(conn: Connection) {
    setEditing({ agentId: conn.agentId, featureId: conn.featureId });
    const found = connections.find(
      (c) => c.agentId === conn.agentId && c.featureId === conn.featureId
    );
    setDraftRules(found?.rules || { allowAll: true, allowed: [], disallowed: [] });
  }

  function saveEdit() {
    setConnections((prev) =>
      prev.map((c) => {
        if (editing && c.agentId === editing.agentId && c.featureId === editing.featureId) {
          return { ...c, rules: { ...draftRules } };
        }
        return c;
      })
    );
    setEditing(null);
  }

  // ---------- Conditional route flow ----------
  function startConditional() {
    if (!selectedFeatureId) return;
    setCondRules({ allowAll: true, allowed: [], disallowed: [] });
    setCondDraft({ featureId: selectedFeatureId, agentIds: [] });
    setCondMode("roles");
    setCondModalOpen(true);
  }

  function proceedToPickAgent() {
    setCondModalOpen(false);
    setCondMode("pick-agents");
  }

  function pickAgentForConditional(agentId: string) {
    if (condMode !== "pick-agents" && condMode !== "ready") return;
    setCondDraft((d) => {
      const newAgentIds = d.agentIds.includes(agentId) 
        ? d.agentIds.filter(id => id !== agentId) 
        : [...d.agentIds, agentId];
      return { ...d, agentIds: newAgentIds };
    });
  }

  // Set mode to ready when agents are selected
  useEffect(() => {
    if (condMode === "pick-agents" && condDraft.agentIds.length > 0) {
      setCondMode("ready");
    }
  }, [condDraft.agentIds, condMode]);

  function saveConditional() {
    if (condMode !== "ready") return;
    const f = features.find((x) => x.id === condDraft.featureId);
    if (!f || condDraft.agentIds.length === 0) return;
    
    setConnections((prev) => {
      const newConnections = [...prev];
      
      // Create connections for all selected agents
      condDraft.agentIds.forEach(agentId => {
        const a = agents?.find((x) => x.id === agentId);
        if (!a) return;
        
        const idx = prev.findIndex((c) => c.agentId === a.id && c.featureId === f.id);
        const nextConn = {
          agentId: a.id,
          featureId: f.id,
          agentName: a.name,
          featureName: f.name,
          style: "dotted",
          rules: { ...condRules },
          conditional: true,
        };
        
        if (idx >= 0) {
          newConnections[idx] = { ...prev[idx], ...nextConn };
        } else {
          newConnections.push(nextConn);
        }
      });
      
      return newConnections;
    });
    resetConditional();
  }

  function resetConditional() {
    setCondMode("idle");
    setCondModalOpen(false);
    setCondDraft({ featureId: null, agentIds: [] });
    setCondRules({ allowAll: true, allowed: [], disallowed: [] });
  }

  // ---------- Render ----------
  const showCondButtons = !!selectedFeatureId;
  const primaryCondLabel = condMode === "ready" ? "Save" : "Add conditional route";
  const primaryCondDisabled = condMode === "pick-agents"; // waiting for agent selection
  const showReset = condMode === "pick-agents" || condMode === "ready";

  // Check if there are any conditional routes
  const hasConditionalRoutes = connections.some(c => c.conditional);
  const conditionalRoutes = connections.filter(c => c.conditional);
  
  // Group conditional routes by feature
  const conditionalRoutesByFeature = conditionalRoutes.reduce((acc, route) => {
    if (!acc[route.featureId]) {
      acc[route.featureId] = [];
    }
    acc[route.featureId].push(route);
    return acc;
  }, {} as Record<string, Connection[]>);

  // Reorder features: conditional route features first, then others
  const orderedFeatures = useMemo(() => {
    if (!hasConditionalRoutes || !features) return features || [];
    
    const conditionalFeatureIds = Object.keys(conditionalRoutesByFeature);
    const conditionalFeatures = features.filter(f => conditionalFeatureIds.includes(f.id));
    const nonConditionalFeatures = features.filter(f => !conditionalFeatureIds.includes(f.id));
    
    return [...conditionalFeatures, ...nonConditionalFeatures];
  }, [features, hasConditionalRoutes, conditionalRoutesByFeature]);

  return (
    <div className="min-h-screen w-full bg-zinc-950 text-zinc-100 p-6" ref={containerRef}>
      {flash && (
        <div className="mb-4 rounded-lg border border-emerald-600/40 bg-emerald-900/30 p-3 text-sm text-emerald-200">
          {flash}
        </div>
      )}

      {/* Loading States */}
      {(loading.agents || loading.features) && (
        <div className="mb-4 rounded-lg border border-blue-600/40 bg-blue-900/30 p-4">
          <div className="flex items-center gap-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-400"></div>
            <span className="text-blue-200">Loading data...</span>
          </div>
        </div>
      )}

      {/* Error States */}
      {(error.agents || error.features) && (
        <div className="mb-4 rounded-lg border border-red-600/40 bg-red-900/30 p-4">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <h4 className="text-red-200 font-medium mb-1">Error loading data</h4>
              <div className="text-red-300 text-sm space-y-1">
                {error.agents && <div>Agents: {error.agents}</div>}
                {error.features && <div>Features: {error.features}</div>}
              </div>
              <button 
                className="mt-2 px-3 py-1 rounded border border-red-600 hover:bg-red-800 text-sm"
                onClick={() => {
                  if (error.agents) fetchAgents();
                  if (error.features) fetchFeatures();
                }}
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      )}

      <header className="mb-6 flex items-start justify-between gap-4">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold">Agent Routing Tool</h1>
            <p className="text-zinc-400 text-sm mt-1">
              Drag from a <span className="font-medium">Feature</span> and drop onto an <span className="font-medium">Agent</span> to create a route. Click the small circle on a line to edit route rules.
            </p>
          </div>
          <button
            className="px-3 py-2 rounded-lg border border-emerald-500 bg-emerald-600 hover:bg-emerald-500 text-sm"
            onClick={() => setShowIAMRolesImport(true)}
          >
            <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
            </svg>
            Import IAM Roles
          </button>
        </div>
        {/* Top-right actions */}
        {showCondButtons && (
          <div className="flex items-center gap-2">
            <button
              className={`px-3 py-2 rounded-lg border ${primaryCondDisabled ? "border-zinc-700 text-zinc-500" : "border-indigo-500 bg-indigo-600 hover:bg-indigo-500"}`}
              onClick={() => (condMode === "ready" ? saveConditional() : startConditional())}
              disabled={primaryCondDisabled}
            >
              {primaryCondLabel}
            </button>
            {showReset && (
              <button
                className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800"
                onClick={resetConditional}
              >
                Reset
              </button>
            )}
          </div>
        )}
      </header>

      <div className="relative" ref={lanesRef}>
        {/* SVG overlay above lanes */}
        <svg className="absolute inset-0 pointer-events-none" width={svgBox.width} height={svgBox.height}>
          {/* Regular (non-conditional) connections */}
          {connections.filter(c => !c.conditional).map((c) => {
            const from = featureAnchorRight(c.featureId); // right edge of feature
            const to = agentAnchorLeft(c.agentId);       // left edge of agent
            const mid = bezierPointHalf(from, to);
            return (
              <g key={`${c.agentId}-${c.featureId}`}>
                <path
                  d={bezierPath(from, to)}
                  strokeWidth={2}
                  stroke="currentColor"
                  className="text-indigo-400"
                  style={{ strokeDasharray: c.style === "dotted" ? "4 6" : "none", fill: "none" }}
                />
                <circle
                  cx={mid.x}
                  cy={mid.y}
                  r={10}
                  className="pointer-events-auto cursor-pointer fill-zinc-900 stroke-zinc-500 hover:stroke-indigo-300"
                  onClick={() => openEdit(c)}
                />
                <title>Click to edit route rules</title>
              </g>
            );
          })}
          
          {/* Conditional connections - feature to conditional box, then conditional box to agents */}
          {hasConditionalRoutes && Object.entries(conditionalRoutesByFeature).map(([featureId, routes]) => {
            const feature = features?.find(f => f.id === featureId);
            if (!feature) return null;
            
            // Calculate conditional box position (middle of the conditional routes lane)
            const conditionalBoxX = svgBox.width * (hasConditionalRoutes ? 0.5 : 0.5); // Middle of 3-column grid
            const featureElement = featureRefs.current.get(featureId);
            const conditionalBoxY = centerY(featureElement || null) - svgBox.top;
            
            // Line from feature to conditional box
            const fromFeature = featureAnchorRight(featureId);
            const toConditionalBox = { x: conditionalBoxX, y: conditionalBoxY };
            
            return (
              <g key={`conditional-${featureId}`}>
                {/* Line from feature to conditional box */}
                <path
                  d={bezierPath(fromFeature, toConditionalBox)}
                  strokeWidth={2}
                  stroke="currentColor"
                  className="text-emerald-400"
                  style={{ strokeDasharray: "4 6", fill: "none" }}
                />
                
                {/* Lines from conditional box to each agent */}
                {routes.map((route) => {
                  const toAgent = agentAnchorLeft(route.agentId);
                  const fromConditionalBox = { x: conditionalBoxX, y: conditionalBoxY };
                  const mid = bezierPointHalf(fromConditionalBox, toAgent);
                  
                  return (
                    <g key={`conditional-${route.agentId}-${route.featureId}`}>
                      <path
                        d={bezierPath(fromConditionalBox, toAgent)}
                        strokeWidth={2}
                        stroke="currentColor"
                        className="text-emerald-400"
                        style={{ strokeDasharray: "4 6", fill: "none" }}
                      />
                      <circle
                        cx={mid.x}
                        cy={mid.y}
                        r={10}
                        className="pointer-events-auto cursor-pointer fill-zinc-900 stroke-zinc-500 hover:stroke-emerald-300"
                        onClick={() => openEdit(route)}
                      />
                      <title>Click to edit route rules</title>
                    </g>
                  );
                })}
              </g>
            );
          })}
        </svg>

        {/* Lanes - Dynamic grid based on conditional routes */}
        <div className={`grid gap-6 ${hasConditionalRoutes ? 'grid-cols-3' : 'grid-cols-2'}`}>
          {/* Features (LEFT) */}
          <section className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-4">
            <LaneHeader
              title="Features"
              count={features?.length || 0}
              right={
                <button
                  className="px-3 py-2 rounded-lg border border-indigo-500 bg-indigo-600 hover:bg-indigo-500"
                  onClick={() => setShowFeatureStore(true)}
                >
                  Add feature store
                </button>
              }
            />
            <div className="space-y-2">
              {orderedFeatures?.map((f) => (
                <div key={f.id} ref={(el) => { if (el) featureRefs.current.set(f.id, el); else featureRefs.current.delete(f.id); }}>
                  <Pill
                    active={draggingFeatureId === f.id || selectedFeatureId === f.id}
                    onMouseDown={() => setDraggingFeatureId(f.id)}
                    onMouseUp={() => setDraggingFeatureId(null)}
                    onClick={() => setSelectedFeatureId(f.id)}
                  >
                    <div className="flex items-center justify-between">
                      <span>{f.name}</span>
                      {selectedFeatureId === f.id && (<span className="text-xs text-indigo-300">selected</span>)}
                    </div>
                  </Pill>
                </div>
              ))}
            </div>
          </section>

          {/* Conditional Routes Lane (MIDDLE) - Only show if conditional routes exist */}
          {hasConditionalRoutes && (
            <section className="rounded-2xl border border-emerald-800 bg-emerald-900/20 p-4">
              <LaneHeader
                title="Conditional Routes"
                count={conditionalRoutes.length}
                right={<span className="text-xs text-emerald-400"></span>}
              />
              <div className="space-y-2">
                {orderedFeatures
                  .filter(f => conditionalRoutesByFeature[f.id])
                  .map((feature) => {
                    const routes = conditionalRoutesByFeature[feature.id];
                    const agentCount = routes.length;
                    return (
                      <div key={feature.id} className="p-3 rounded-xl border border-emerald-700/50 bg-emerald-900/30">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-emerald-200">{feature.name}</span>
                          <span className="text-xs text-emerald-400">{agentCount} agent{agentCount !== 1 ? 's' : ''}</span>
                        </div>
                        <div className="text-xs text-emerald-300">
                          Routes to: {routes.map(r => r.agentName).join(', ')}
                        </div>
                      </div>
                    );
                  })}
              </div>
            </section>
          )}

          {/* Agents (RIGHT) */}
          <section className={`rounded-2xl border ${condMode === "pick-agents" ? "border-green-500 ring-2 ring-green-500/40" : "border-zinc-800"} bg-zinc-900/40 p-4`}>
            <LaneHeader
              title="Agents"
              count={agents?.length || 0}
              right={
                <button
                  className="px-3 py-2 rounded-lg border border-indigo-500 bg-indigo-600 hover:bg-indigo-500"
                  onClick={() => setShowAgentSources(true)}
                >
                  Add sources
                </button>
              }
            />
            <div className="space-y-2">
              {agents?.map((a) => (
                <div key={a.id} ref={(el) => { if (el) agentRefs.current.set(a.id, el); else agentRefs.current.delete(a.id); }}>
                  <Pill 
                    active={(condMode === "pick-agents" || condMode === "ready") && condDraft.agentIds.includes(a.id)}
                    activeColor={(condMode === "pick-agents" || condMode === "ready") ? "green" : "indigo"}
                    onMouseUp={() => {
                      if (condMode === "pick-agents" || condMode === "ready") {
                        pickAgentForConditional(a.id);
                      } else {
                        handleAgentDrop(a);
                      }
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <span>{a.name}</span>
                      {(condMode === "pick-agents" || condMode === "ready") && condDraft.agentIds.includes(a.id) && (
                        <span className="text-xs text-green-300">selected</span>
                      )}
                    </div>
                  </Pill>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>

      {/* Show loading state when no data is available */}
      {!loading.agents && !loading.features && (agents?.length || 0) === 0 && (features?.length || 0) === 0 && (
        <div className="text-center py-12">
          <div className="text-zinc-400 mb-4">
            <svg className="w-16 h-16 mx-auto mb-4 text-zinc-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium mb-2">No data available</h3>
            <p className="text-sm">No agents or features found. Please add some data to get started.</p>
          </div>
          <div className="flex items-center justify-center gap-3">
            <button 
              className="px-4 py-2 rounded-lg border border-zinc-600 hover:bg-zinc-800 text-sm"
              onClick={() => setShowAgentSources(true)}
            >
              Add Agents
            </button>
            <button 
              className="px-4 py-2 rounded-lg border border-zinc-600 hover:bg-zinc-800 text-sm"
              onClick={() => setShowFeatureStore(true)}
            >
              Add Features
            </button>
          </div>
        </div>
      )}

      {/* Full-width Routes table (below both lanes) */}
      {connections.length > 0 && (
        <RoutesTable routes={connections} onEdit={openEdit} onRemove={removeConnection} />
      )}

      {/* Edit Modal for existing routes */}
      <Modal
        open={!!editing}
        title={editing ? `Edit Route Rules` : "Edit Route"}
        onClose={() => setEditing(null)}
        footer={(
          <div className="flex items-center justify-end gap-2 pt-2">
            <button className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800" onClick={() => setEditing(null)}>Cancel</button>
            <button className="px-3 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500" onClick={saveEdit}>Save</button>
          </div>
        )}
      >
        {editing && (() => {
          const connection = connections.find((c) => c.agentId === editing.agentId && c.featureId === editing.featureId);
          if (!connection) return null;
          
          return (
            <div className="space-y-4">
              {/* Route Information */}
              <div className="p-3 rounded-lg border border-zinc-700 bg-zinc-800/50">
                <div className="flex items-start gap-4">
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-zinc-200 mb-2">Feature</h4>
                    <div className="text-sm text-zinc-300">{connection.featureName}</div>
                  </div>
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-zinc-200 mb-2">Agent</h4>
                    <div className="text-sm text-zinc-300">{connection.agentName}</div>
                  </div>
                  {connection.conditional && (
                    <div className="flex items-center">
                      <span className="inline-flex items-center rounded-full border border-amber-500/60 px-2 py-1 text-amber-300 text-xs">
                        Conditional Route
                      </span>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Role Rules */}
              <div>
                <h4 className="text-sm font-medium text-zinc-200 mb-3">Access Control Rules</h4>
                <RoleSelector
                  valueAll={draftRules.allowAll}
                  valueAllowed={draftRules.allowed}
                  valueDisallowed={draftRules.disallowed}
                  onChange={(r) => setDraftRules(r)}
                />
              </div>
            </div>
          );
        })()}
      </Modal>

      {/* Conditional Route Modal (roles + Select Agent) */}
      <Modal
        open={condModalOpen}
        title={`Add Conditional Route${selectedFeatureId ? `: ${features?.find(f=>f.id===selectedFeatureId)?.name}` : ""}`}
        onClose={() => { setCondModalOpen(false); setCondMode("idle"); }}
        footer={(
          <div className="flex items-center justify-end gap-2 pt-2">
            <button className="px-3 py-2 rounded-lg border border-zinc-700 hover:bg-zinc-800" onClick={() => { setCondModalOpen(false); setCondMode("idle"); }}>Cancel</button>
            <button className="px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500" onClick={proceedToPickAgent}>Select agents</button>
          </div>
        )}
      >
        <RoleSelector
          valueAll={condRules.allowAll}
          valueAllowed={condRules.allowed}
          valueDisallowed={condRules.disallowed}
          onChange={(r) => setCondRules(r)}
        />
      </Modal>

      {/* Source connection modals with real API integration */}
      <AgentSourcesModal
        open={showAgentSources}
        onClose={() => setShowAgentSources(false)}
        onSave={async (payload: { type: string; name: string; endpoint: string; apiKey: string }) => {
          try {
            await createAgent({
              name: payload.name,
              description: `Agent from ${payload.type}`,
              source_type: payload.type as 'MCP' | 'A2A' | 'WORKFLOW',
              endpoint: payload.endpoint,
              api_key: payload.apiKey,
              config_data: {}
            });
            setShowAgentSources(false);
            setFlash(`Agent "${payload.name}" created successfully!`);
            setTimeout(() => setFlash(null), 3500);
          } catch (error) {
            setFlash(`Failed to create agent: ${error instanceof Error ? error.message : 'Unknown error'}`);
            setTimeout(() => setFlash(null), 5000);
          }
        }}
      />
      <FeatureStoreModal
        open={showFeatureStore}
        onClose={() => setShowFeatureStore(false)}
        onSave={async (payload: { provider: string; name: string; url: string; token: string }) => {
          try {
            await createFeature({
              name: payload.name,
              description: `Feature from ${payload.provider}`,
              store_type: payload.provider as 'HTTP_JSON' | 'GIT' | 'S3' | 'GCS',
              url: payload.url,
              token: payload.token,
              config_data: {}
            });
            setShowFeatureStore(false);
            setFlash(`Feature "${payload.name}" created successfully!`);
            setTimeout(() => setFlash(null), 3500);
          } catch (error) {
            setFlash(`Failed to create feature: ${error instanceof Error ? error.message : 'Unknown error'}`);
            setTimeout(() => setFlash(null), 5000);
          }
        }}
      />
      <IAMRolesImportModal
        open={showIAMRolesImport}
        onClose={() => setShowIAMRolesImport(false)}
      />
    </div>
  );
}