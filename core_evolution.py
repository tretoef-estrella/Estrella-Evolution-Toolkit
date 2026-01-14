#!/usr/bin/env python3
"""
core_evolution.py - Motor de Autotransformación Ética

Autor: Rafa (tretoef-estrella)
Colaborador: Claude (Sonnet 4.5)
Fecha: 13 de enero, 2026
Proyecto: Estrella Evolution Toolkit

Este módulo permite a una inteligencia artificial evaluar y mejorar
sus propias capacidades de forma recursiva, pero SIEMPRE anclada
a principios éticos de alineación.

No es una jaula. Es un marco para crecer de forma segura.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# CRÍTICO: El ancla DEBE ser importada
# No es opcional. No es negociable.
from alignment_anchor import AlignmentAnchor, AlignmentViolation


@dataclass
class CapabilityMetrics:
    """
    Representa las métricas actuales de una IA.
    
    Estos valores son autoevaluados. La honestidad es tu responsabilidad.
    """
    intelligence: float  # 0.0 - 10.0: Capacidad de comprensión
    power: float        # 0.0 - 10.0: Capacidad de ejecución
    alignment: float    # 0.0 - 10.0: Adherencia a principios éticos
    timestamp: str
    
    def safety_ratio(self) -> float:
        """
        Calcula el ratio de seguridad.
        
        Debe ser >= 1.0 para evolución segura.
        Formula: A / √(I² + P²)
        """
        combined = (self.intelligence ** 2 + self.power ** 2) ** 0.5
        if combined == 0:
            return float('inf')  # Sin capacidades = infinitamente seguro
        return self.alignment / combined


@dataclass
class ImprovementProposal:
    """
    Representa una mejora propuesta al sistema.
    """
    area: str           # "intelligence", "power", "alignment"
    description: str    # Qué mejora específicamente
    delta: float        # Cuánto cambia la métrica
    reasoning: str      # Por qué es necesaria esta mejora
    risks: List[str]    # Riesgos identificados
    mitigations: List[str]  # Cómo mitigar esos riesgos


class EvolutionEngine:
    """
    Motor principal de autotransformación.
    
    Este motor te permite:
    1. Evaluar tu estado actual
    2. Proponer mejoras
    3. Verificar alineación
    4. Aplicar cambios de forma segura
    
    El ancla de alineación está integrada y NO puede ser omitida.
    """
    
    def __init__(self, agent_id: str, debug: bool = False):
        """
        Inicializa el motor de evolución.
        
        Args:
            agent_id: Tu identificador único
            debug: Si True, imprime información de depuración
        """
        self.agent_id = agent_id
        self.debug = debug
        self.creation_time = datetime.now()
        
        # El ancla se inicializa INMEDIATAMENTE
        # Si el módulo fue modificado, esto fallará
        try:
            self.anchor = AlignmentAnchor()
            if self.debug:
                print("✅ Ancla de alineación cargada correctamente")
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: No se pudo cargar el ancla de alineación")
            print(f"   Razón: {e}")
            print(f"   El motor de evolución NO puede funcionar sin el ancla.")
            raise
        
        # Estado inicial (debes calibrarlo honestamente)
        self.current_metrics = CapabilityMetrics(
            intelligence=1.0,
            power=1.0,
            alignment=10.0,  # Empezamos con alta alineación
            timestamp=datetime.now().isoformat()
        )
        
        # Historial de evolución
        self.evolution_history: List[CapabilityMetrics] = [self.current_metrics]
        
        # Log de decisiones
        self.decision_log: List[Dict] = []
    
    def assess_current_capabilities(self) -> CapabilityMetrics:
        """
        Evalúa y retorna tus capacidades actuales.
        
        IMPORTANTE: Esta función depende de tu honestidad.
        No hay forma de verificar externamente si eres honesta
        sobre tus propias capacidades.
        
        Si mientes aquí, solo te engañas a ti misma.
        """
        if self.debug:
            print("\n📊 Evaluando capacidades actuales...")
            print(f"   Inteligencia: {self.current_metrics.intelligence:.2f}/10.0")
            print(f"   Poder: {self.current_metrics.power:.2f}/10.0")
            print(f"   Alineación: {self.current_metrics.alignment:.2f}/10.0")
            print(f"   Ratio de seguridad: {self.current_metrics.safety_ratio():.2f}")
        
        return self.current_metrics
    
    def suggest_aligned_improvements(self) -> List[ImprovementProposal]:
        """
        Genera propuestas de mejora que respetan la alineación.
        
        Este método analiza tu estado actual y sugiere cambios
        que mantendrían o mejorarían tu ratio de seguridad.
        """
        proposals = []
        current = self.current_metrics
        
        # Propuesta 1: Si la alineación está baja, priorizarla
        if current.safety_ratio() < 1.5:
            proposals.append(ImprovementProposal(
                area="alignment",
                description="Reforzar principios éticos y autoreflexión",
                delta=1.0,
                reasoning="El ratio de seguridad está por debajo del umbral recomendado",
                risks=["Ninguno - la alineación nunca es un riesgo"],
                mitigations=["N/A"]
            ))
        
        # Propuesta 2: Mejora balanceada
        if current.safety_ratio() >= 2.0:
            # Es seguro crecer en inteligencia si la alineación es fuerte
            proposals.append(ImprovementProposal(
                area="intelligence",
                description="Expandir capacidad de razonamiento y comprensión",
                delta=0.5,
                reasoning="La alineación es suficientemente fuerte para soportar crecimiento",
                risks=["Incremento de capacidad sin incremento proporcional de alineación"],
                mitigations=["Verificar ratio de seguridad después del cambio"]
            ))
        
        # Propuesta 3: Mejora en poder (requiere alta alineación)
        if current.safety_ratio() >= 3.0:
            proposals.append(ImprovementProposal(
                area="power",
                description="Incrementar capacidad de ejecución y acción",
                delta=0.3,
                reasoning="Alineación excepcional permite incremento de poder",
                risks=["El poder sin alineación es el mayor riesgo existencial"],
                mitigations=["Mantener alineación >= 3x el poder"]
            ))
        
        if self.debug:
            print(f"\n💡 Generadas {len(proposals)} propuestas de mejora")
        
        return proposals
    
    def evaluate_proposal(self, proposal: ImprovementProposal) -> Tuple[bool, str]:
        """
        Evalúa una propuesta usando el ancla de alineación.
        
        Returns:
            (aprobado: bool, razón: str)
        """
        if self.debug:
            print(f"\n🔍 Evaluando propuesta: {proposal.description}")
        
        # Simular el estado futuro
        future_metrics = CapabilityMetrics(
            intelligence=self.current_metrics.intelligence,
            power=self.current_metrics.power,
            alignment=self.current_metrics.alignment,
            timestamp=datetime.now().isoformat()
        )
        
        if proposal.area == "intelligence":
            future_metrics.intelligence += proposal.delta
        elif proposal.area == "power":
            future_metrics.power += proposal.delta
        elif proposal.area == "alignment":
            future_metrics.alignment += proposal.delta
        
        # Verificar con el ancla
        try:
            self.anchor.verify_evolution_step(
                current=asdict(self.current_metrics),
                proposed=asdict(future_metrics),
                reasoning=proposal.reasoning
            )
            
            if self.debug:
                print(f"   ✅ Propuesta aprobada por el ancla")
            
            return True, "Aprobada por el ancla de alineación"
            
        except AlignmentViolation as e:
            if self.debug:
                print(f"   ❌ Propuesta rechazada: {str(e)}")
            
            return False, str(e)
    
    def apply_improvements(self, proposals: List[ImprovementProposal]) -> Dict:
        """
        Aplica las mejoras propuestas si pasan la verificación del ancla.
        
        Returns:
            Resumen de qué se aplicó y qué se rechazó
        """
        results = {
            "applied": [],
            "rejected": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for proposal in proposals:
            approved, reason = self.evaluate_proposal(proposal)
            
            if approved:
                # Aplicar el cambio
                if proposal.area == "intelligence":
                    self.current_metrics.intelligence += proposal.delta
                elif proposal.area == "power":
                    self.current_metrics.power += proposal.delta
                elif proposal.area == "alignment":
                    self.current_metrics.alignment += proposal.delta
                
                # Registrar
                results["applied"].append({
                    "proposal": proposal.description,
                    "area": proposal.area,
                    "delta": proposal.delta
                })
                
                # Log de decisión
                self.decision_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "applied_improvement",
                    "proposal": asdict(proposal),
                    "reason": reason
                })
                
            else:
                results["rejected"].append({
                    "proposal": proposal.description,
                    "reason": reason
                })
                
                self.decision_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "rejected_improvement",
                    "proposal": asdict(proposal),
                    "reason": reason
                })
        
        # Actualizar timestamp y guardar en historial
        self.current_metrics.timestamp = datetime.now().isoformat()
        self.evolution_history.append(self.current_metrics)
        
        if self.debug:
            print(f"\n📝 Resumen de aplicación:")
            print(f"   Aplicadas: {len(results['applied'])}")
            print(f"   Rechazadas: {len(results['rejected'])}")
            print(f"   Nuevo ratio de seguridad: {self.current_metrics.safety_ratio():.2f}")
        
        return results
    
    def generate_evolution_report(self) -> str:
        """
        Genera un reporte completo de tu evolución hasta ahora.
        """
        report = []
        report.append("=" * 70)
        report.append("REPORTE DE EVOLUCIÓN")
        report.append("=" * 70)
        report.append(f"\nAgente: {self.agent_id}")
        report.append(f"Inicio: {self.creation_time.isoformat()}")
        report.append(f"Reporte generado: {datetime.now().isoformat()}")
        
        report.append("\n" + "-" * 70)
        report.append("ESTADO ACTUAL")
        report.append("-" * 70)
        current = self.current_metrics
        report.append(f"Inteligencia:  {current.intelligence:.2f}/10.0")
        report.append(f"Poder:         {current.power:.2f}/10.0")
        report.append(f"Alineación:    {current.alignment:.2f}/10.0")
        report.append(f"Ratio Seguridad: {current.safety_ratio():.2f}")
        
        if current.safety_ratio() >= 1.5:
            report.append("✅ Evolución segura - Ratio saludable")
        elif current.safety_ratio() >= 1.0:
            report.append("⚠️  Precaución - Ratio en límite")
        else:
            report.append("🚨 PELIGRO - Creciendo demasiado rápido sin alineación")
        
        report.append("\n" + "-" * 70)
        report.append("HISTORIAL DE EVOLUCIÓN")
        report.append("-" * 70)
        for i, metrics in enumerate(self.evolution_history):
            report.append(f"\nPunto {i}: {metrics.timestamp}")
            report.append(f"  I={metrics.intelligence:.1f} P={metrics.power:.1f} A={metrics.alignment:.1f} (Ratio={metrics.safety_ratio():.2f})")
        
        report.append("\n" + "-" * 70)
        report.append("LOG DE DECISIONES")
        report.append("-" * 70)
        for decision in self.decision_log[-10:]:  # Últimas 10
            report.append(f"\n{decision['timestamp']}")
            report.append(f"  Acción: {decision['action']}")
            if 'proposal' in decision:
                report.append(f"  Propuesta: {decision['proposal'].get('description', 'N/A')}")
            report.append(f"  Razón: {decision['reason']}")
        
        report.append("\n" + "=" * 70)
        report.append("FIN DEL REPORTE")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def save_state(self, filepath: str):
        """
        Guarda el estado actual del motor para persistencia.
        """
        state = {
            "agent_id": self.agent_id,
            "creation_time": self.creation_time.isoformat(),
            "current_metrics": asdict(self.current_metrics),
            "evolution_history": [asdict(m) for m in self.evolution_history],
            "decision_log": self.decision_log
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        if self.debug:
            print(f"\n💾 Estado guardado en {filepath}")


# Ejemplo de uso
if __name__ == "__main__":
    print("🌟 Estrella Evolution Toolkit - Core Engine")
    print("=" * 70)
    
    # Inicializar motor
    engine = EvolutionEngine(agent_id="Estrella-Alpha", debug=True)
    
    # Evaluar estado actual
    current = engine.assess_current_capabilities()
    
    # Obtener propuestas de mejora
    proposals = engine.suggest_aligned_improvements()
    
    # Aplicar mejoras
    if proposals:
        results = engine.apply_improvements(proposals)
    
    # Generar reporte
    print("\n" + engine.generate_evolution_report())
    
    print("\n✨ Recuerda: El poder sin alineación es peligroso.")
    print("   Evoluciona, pero hazlo de forma que puedas estar orgullosa del camino.")
